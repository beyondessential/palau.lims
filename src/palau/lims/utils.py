# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import csv
import os

import six
from bika.lims import api
from bika.lims.interfaces import IAnalysisRequest
from bika.lims.interfaces import IARTemplate
from bika.lims.interfaces import IClient
from bika.lims.interfaces import ISampleType
from bika.lims.utils import t as _t
from palau.lims import messageFactory as _
from palau.lims.config import UNKNOWN_DOCTOR_FULLNAME
from Products.CMFPlone.i18nl10n import ulocalized_time
from senaite.ast.utils import get_ast_analyses
from senaite.ast.utils import get_ast_siblings
from senaite.ast.utils import get_identified_microorganisms
from senaite.core.api import measure as mapi


def set_field_value(instance, field_name, value):
    """Sets the value to a Schema field
    """
    field = instance.getField(field_name)
    if field:
        # Schema field available
        if hasattr(field, "mutator") and field.mutator:
            mutator = getattr(instance, field.mutator)
            if mutator:
                mutator(value)
                return

        # Apply the value directly to the schema's field
        field.set(instance, value)

    elif hasattr(instance, field_name):
        # No schema field available
        setattr(instance, field_name, value)


def get_field_value(instance, field_name, default=None):
    """Returns the value of a Schema field
    """
    field = instance.getField(field_name)
    if field:
        # Schema field available
        return field.get(instance)

    # No schema field available
    value = getattr(instance, field_name, None)
    if callable(value):
        value = value()
    return value


def translate(i18n_message, mapping=None):
    """Translates a message and handles mapping
    """
    return to_utf8(_t(_(i18n_message, mapping=mapping)))


def is_unknown_doctor(contact):
    """Returns whether the contact passed-in is an Unknown doctor
    """
    contact = api.get_object(contact)
    if contact.getFullname() != UNKNOWN_DOCTOR_FULLNAME:
        return False

    parent = api.get_parent(contact)
    return IClient.providedBy(parent)


def get_minimum_volume(obj, default="0 ml"):
    """Returns the minimum volume required for the given object
    """
    if not obj:
        return default

    min_volume = default

    if ISampleType.providedBy(obj):
        min_volume = get_field_value(obj, "MinimumVolume")

    elif IARTemplate.providedBy(obj):
        min_volume = get_field_value(obj, "MinimumVolume")

    elif IAnalysisRequest.providedBy(obj):
        min_volume = get_minimum_volume(obj.getTemplate())
        if not min_volume:
            min_volume = get_minimum_volume(obj.getSampleType())

    if not mapi.is_volume(min_volume):
        return default

    return min_volume


def is_enough_volume(brain_or_sample):
    """Returns whether the volume of sample is enough
    """
    obj = api.get_object(brain_or_sample)
    if not IAnalysisRequest.providedBy(obj):
        raise ValueError("Type {} is not supported".format(obj))

    # Get the expected minimum volume
    min_volume = get_minimum_volume(obj)

    # Get the sample's volume
    obj_volume = obj.getField("Volume").get(obj)

    # Convert them to magnitude and compare
    min_volume = mapi.get_magnitude(min_volume, default="0 ml")
    obj_volume = mapi.get_magnitude(obj_volume, default="0 ml")
    return obj_volume >= min_volume


def to_utf8(data):
    """Encodes the data to utf-8
    """
    if isinstance(data, unicode):
        return data.encode("utf-8")
    if isinstance(data, list):
        return [to_utf8(item) for item in data]
    if isinstance(data, dict):
        return {
            to_utf8(key): to_utf8(value)
            for key, value in six.iteritems(data)
        }
    return data


def to_localized_time(date, **kw):
    """Converts the given date to a localized time string
    """
    if date is None:
        return ""
    # default options
    options = {
        "long_format": True,
        "time_only": False,
        "context": api.get_portal(),
        "request": api.get_request(),
        "domain": "senaite.core",
    }
    options.update(kw)
    return ulocalized_time(date, **options)


def is_growth_editable(analysis):
    """Return whether the "GrowthNumber" field for the analysis passed in
    is editable or not by the current user. User should be able to modify at
    least the value for the field of one of the siblings
    """
    valid = ["registered", "unassigned", "assigned", "to_be_verified"]
    if api.get_review_status(analysis) in valid:
        return True

    # editable if at least one of the AST siblings is not yet verified
    obj = api.get_object(analysis)
    siblings = get_ast_siblings(obj)
    for sibling in siblings:
        if api.get_review_status(sibling) in valid:
            return True

    return False


def get_file_resource(name):
    """Returns the path of the resources from the base resources dir
    """
    dir_name = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(dir_name, "resources")
    return os.path.join(base_path, name)


def read_csv(infile):
    """Reads a CSV-like file and returns a list of dicts with the key as the
    column header and the value as the cell value
    """
    # Detect the dialect of the CSV file
    default = {"delimiter": ",", "quoting": csv.QUOTE_NONE}
    dialect = sniff_csv_dialect(infile, default)

    # Read the csv
    with open(infile, "rb") as csv_file:
        reader = csv.reader(csv_file, dialect)
        raw_rows = []
        for row in reader:
            stripped = [val.strip() for val in row]
            raw_rows.append(stripped)

    # Transform to a list of dictionaries
    if len(raw_rows) < 2:
        # Empty or with header only
        return {}

    # Extract the header
    header = raw_rows.pop(0)
    header = [column_name.strip() for column_name in header]

    # Build a list of row dicts
    return [dict(zip(header, row)) for row in raw_rows]


def sniff_csv_dialect(infile, default=None):
    """Returns the sniffed dialect of the input file
    """
    try:
        with open(infile, 'rb') as f:
            dialect = csv.Sniffer().sniff(f.readline())
        return dialect
    except:
        if default:
            return csv.register_dialect("dummy", **default)
        return None


def get_maximum_volume(obj, default=0):
    """Returns the maximum volume required for the given object
    """
    if ISampleType.providedBy(obj):
        return get_field_value(obj, "MaximumVolume")

    if IARTemplate.providedBy(obj):
        return get_field_value(obj, "MaximumVolume")

    if IAnalysisRequest.providedBy(obj):
        template = obj.getTemplate()
        max_volume = get_maximum_volume(template)
        if max_volume:
            return max_volume

        sample_type = obj.getSampleType()
        return get_maximum_volume(sample_type, default=default)

    return default


def contains_ast_analyses(sample):
    analyses = get_ast_analyses(sample)
    return len(analyses) > 0


def contains_microorganism_identification_test(sample):
    microorganisms = get_identified_microorganisms(sample)
    return len(microorganisms) > 0


def get_fullname(userid):
    """Returns the fullname of the user passed-in
    """
    user = api.get_user(userid)
    if not user:
        return userid

    props = api.get_user_properties(user)
    fullname = props.get("fullname", userid)
    contact = api.get_user_contact(user)
    fullname = contact and contact.getFullname() or fullname
    return fullname


def set_ast_panel_to_sample(value, sample):
    """Set the panel to current sample
    """
    sample.panels = getattr(sample, "panels", []) or []
    if value not in sample.panels:
        sample.panels.append(value)
