# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS.
#
# PALAU.LIMS is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2023-2025 by it's authors.
# Some rights reserved, see README and LICENSE.

import argparse
import csv
import logging
import os
from datetime import datetime
from datetime import timedelta
from time import time

import transaction
from bes.lims.scripts import setup_script_environment
from bika.lims import api
from bika.lims.api import security as sapi
from palau.lims import logger
from bes.lims.tamanu.config import TAMANU_USER
from Products.CMFCore.permissions import ModifyPortalContent
from senaite.core.api import dtime
from senaite.core.api.dtime import to_localized_time
from senaite.core.schema.addressfield import PHYSICAL_ADDRESS
from senaite.patient import api as patient_api

COLUMNS_TO_FIELDS = (
    # List of tuples of (column_title, patient_field_name)
    ("Code", "mrn"),
    ("Last name", "lastname"),
    ("First name", "firstname"),
    ("Date of birth", "birthdate"),
    ("Gender", "sex"),
    ("Email", "email"),
)


parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-f", "--file",
                    help="File with the patients in csv format")

parser.add_argument("-v", "--verbose", action="store_true",
                    help="Verbose logging")


def sniff_csv_dialect(infile, default=None):
    """Returns the sniffed dialect of the input file
    """
    try:
        with open(infile, 'rb') as f:
            dialect = csv.Sniffer().sniff(f.readline())

        return dialect
    except:  # noqa
        if default:
            return csv.register_dialect("dummy", **default)

        return None


def read_raw_rows_from_csv(infile):
    """Reads the input file and returns a list of lists
    """
    # Detect the dialect of the CSV file
    default = {"delimiter": ",", "quoting": csv.QUOTE_NONE}
    dialect = sniff_csv_dialect(infile, default)

    # Read the csv
    with open(infile, "rb") as csv_file:
        reader = csv.reader(csv_file, dialect)
        raw_rows = map(lambda row: row, reader) or []

    return raw_rows


def read_csv(infile):
    """Reads the csv and returns the data back as list of dicts, where each
    record is a row from the csv file represented as a dict, with the key as
    the column name and the value as the value of the column
    """
    rows = read_raw_rows_from_csv(infile)

    if len(rows) < 2:
        return []

    header = rows[0]

    return map(lambda row: dict(zip(header, row)), rows[1:])


def get_sex_id(value):
    """returns a valid sex id
    """
    target = value.strip().lower() if value else ""
    mapping = {"true": "f", "false": "m"}
    target = mapping.get(target, target)
    if target in "fm":
        return target
    return ""


def get_empty_address(address_type):
    """Returns a dict that represents an empty address for the given type
    """
    return {
        "type": address_type,
        "address": "",
        "zip": "",
        "city": "",
        "subdivision2": "",
        "subdivision1": "",
        "country": "",
    }


def get_patient_values(row):
    """Returns a dict representing a patient from the row passed-in
    """
    mapping = dict(COLUMNS_TO_FIELDS)
    info = dict.fromkeys(mapping.values(), "")
    address_columns = ["Country", "address"]
    address = get_empty_address(PHYSICAL_ADDRESS)

    for column, value in row.items():
        if column in address_columns and value:
            address[column.lower()] = value
            continue

        field_name = mapping.get(column)
        if not field_name:
            continue

        value = value.strip() if value else ""
        if field_name == "birthdate":
            # convert to date time
            value = dtime.to_DT(value)
        elif field_name == "sex":
            # convert to sex id
            value = get_sex_id(value)

        if not value:
            continue

        info[field_name] = value

    info["address"] = [address]
    return info


def get_etd(started, processed, total):
    """Returns the Estimated Time of Delivery datetime
    """
    now = datetime.now()
    delta = now - started
    seconds = (total-processed)*delta.seconds/processed
    return now + timedelta(seconds=seconds)


def import_patients(infile):
    """Reads a CSV file and import the patients
    """
    # get the file modification time
    modified = os.path.getmtime(infile)
    modified = dtime.to_DT(datetime.fromtimestamp(modified))
    patient_folder = api.get_portal().patients
    records = read_csv(infile)
    total = len(records)
    step = 100
    counts = {"updated": 0, "created": 0}
    started = datetime.now()
    for num, record in enumerate(records):
        if num and num % step == 0:
            etd = get_etd(started, num, total)
            etd = to_localized_time(etd, long_format=True)
            logger.info("Importing patients {}/{}. c:{}, u:{}, ETD: {}".format(
                num, total, counts["created"], counts["updated"], etd))
            transaction.commit()

        # get the dict representation of the patient
        values = get_patient_values(record)

        # get the id of the patient
        mrn = values.get("mrn")
        if not mrn:
            logger.error("MRN not defined for {}. [SKIP]".format(repr(record)))
            continue

        # get the patient
        patient = patient_api.get_patient_by_mrn(mrn, include_inactive=True)
        if not patient:
            # create the patient
            patient = api.create(patient_folder, "Patient", **values)
            counts["created"] += 1

        elif patient.modified() < modified:
            # update the patient
            api.edit(patient, check_permissions=False, **values)
            counts["updated"] += 1

        # assign ownership to 'tamanu' user
        creator = patient.Creator()
        if creator != TAMANU_USER:
            sapi.revoke_local_roles_for(patient, roles=["Owner"], user=creator)

        # grant 'Owner' role to the user who is modifying the object
        sapi.grant_local_roles_for(patient, roles=["Owner"], user=TAMANU_USER)

        # don't allow the edition, but to tamanu (Owner) only
        sapi.manage_permission_for(patient, ModifyPortalContent, ["Owner"])

        # re-index object security indexes (e.g. allowedRolesAndUsers)
        patient.reindexObjectSecurity()

        # flush the object from memory
        patient._p_deactivate()


def main(app):
    args, _ = parser.parse_known_args()
    if hasattr(args, "help") and args.help:
        print("")
        parser.print_help()
        parser.exit()

        return

    # Setup environment
    setup_script_environment(app, stream_out=False)

    # verbose logging
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    file_in = args.file
    if not file_in or not os.path.isfile(file_in):
        logger.error("Not a valid file: {}".format(repr(file_in)))

        return

    # do the work
    logger.info("-"*79)
    logger.info("Importing patients from {} ...".format(file_in))
    logger.info("Started: {}".format(datetime.now().isoformat()))
    start = time()

    import_patients(file_in)

    # Commit transaction
    transaction.commit()
    logger.info("Importing patients from {} [DONE]".format(file_in))
    logger.info("Elapsed: {}".format(timedelta(seconds=(time()-start))))
    logger.info("-"*79)


if __name__ == "__main__":
    main(app)  # noqa: F821
