# -*- coding: utf-8 -*-

import argparse
import csv
import logging
import os
import transaction
from bika.lims import api
from datetime import datetime
from datetime import timedelta
from palau.lims import logger
from palau.lims.scripts import setup_script_environment
from senaite.core.api import dtime
from senaite.patient import api as patient_api
from senaite.patient.catalog import PATIENT_CATALOG
from senaite.patient.config import SEXES
from time import time

COLUMNS_TO_FIELDS = (
    # List of tuples of (column_title, patient_field_name)
    ("Code", "mrn"),
    ("Last name", "lastname"),
    ("First name", "firstname"),
    ("Date of birth", "birthdate"),
    ("Gender", "sex"),
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

    for key, val in SEXES:
        if key.lower() == target:
            return key
        if val.lower() == target:
            return key

    return ""


def get_patient_values(row):
    """Returns a dict representing a patient from the row passed-in
    """
    mapping = dict(COLUMNS_TO_FIELDS)
    info = dict.fromkeys(mapping.values(), "")

    for column, value in row.items():
        field_name = mapping.get(column)
        if not field_name:
            logger.warn("No field name declared for column {}".format(column))
            field_name = column

        value = value.strip() if value else ""
        if field_name == "birthdate":
            # convert to date time
            value = dtime.to_DT(value)
        elif field_name == "sex":
            # convert to sex id
            value = get_sex_id(value)

        if not value:
            logger.error("Wrong or empty {}: {}".format(column, repr(row)))
            continue

        info[field_name] = value

    return info


def import_patients(infile):
    """Reads a CSV file and import the patients
    """
    # get all registered mrns
    cat = api.get_tool(PATIENT_CATALOG)
    mrns = cat.uniqueValuesFor("patient_mrn")
    mrns = filter(None, [mrn.strip() for mrn in mrns])
    mrns = dict.fromkeys(mrns, True)

    patient_folder = api.get_portal().patients
    records = read_csv(infile)
    total = len(records)

    for num, record in enumerate(records):
        if num and num % 100 == 0:
            logger.info("Patients imported {}/{}".format(num, total))
            transaction.commit()

        # get the dict representation of the patient
        values = get_patient_values(record)

        # get the id of the patient
        mrn = values.get("mrn")
        if not mrn:
            logger.error("MRN not defined for {}. [SKIP]".format(repr(record)))
            continue

        # get the patient
        patient = patient_api.get_patient_by_mrn(mrn)
        if patient:
            # update the patient
            patient_api.update_patient(patient, **values)
        else:
            # create the patient
            patient = api.create(patient_folder, "Patient", **values)

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
    setup_script_environment(app)

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
    logger.info("Commit transaction ...")
    transaction.commit()
    logger.info("Importing patients from {} [DONE]".format(file_in))
    logger.info("Elapsed: {}".format(timedelta(seconds=(time()-start))))
    logger.info("-"*79)


if __name__ == "__main__":
    main(app)  # noqa: F821
