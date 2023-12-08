# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from bika.lims import deprecated
from palau.lims.config import TARGET_PATIENTS
from palau.lims.utils import get_field_value
from palau.lims.utils import get_file_resource
from palau.lims.utils import read_csv
from senaite.ast.utils import get_identified_microorganisms
from senaite.core.api import dtime
from senaite.core.catalog import SAMPLE_CATALOG
from datetime import datetime


def get_received_samples(from_date, to_date, **kwargs):
    """Returns the primary samples (no Partitions) that were received within
    the passed-in date range and parameters
    """
    query = {
        "portal_type": "AnalysisRequest",
        "isRootAncestor": True,
        "getDateReceived": {
            "query": [from_date, to_date],
            "range": "min:max"
        },
        "sort_on": "getDateReceived",
        "sort_order": "ascending",
    }
    query.update(**kwargs)
    return api.search(query, SAMPLE_CATALOG)


def get_received_samples_by_year(year, **kwargs):
    """Returns the primary samples received within the passed-in year and
    parameters
    """
    from_date = dtime.date_to_string(datetime(year, 1, 1))
    to_date = dtime.date_to_string(datetime(year, 12, 31))
    return get_received_samples(from_date, to_date, **kwargs)


def group_by(objs, func):
    """Group objects by the passed-in function
    """
    groups = {}
    for obj in objs:
        if not hasattr(obj, func) and api.is_brain(obj):
            obj = api.get_object(obj)

        value = getattr(obj, func, None)
        if callable(value):
            value = value()

        if api.is_object(value):
            # group by title
            value = api.get_title(value)

        elif dtime.is_date(value):
            # group by month
            value = int(value.month())

        if isinstance(value, list):
            # in case value is a list of rejection reasons
            map(lambda val: groups.setdefault(val, []).append(obj), value)
        else:
            groups.setdefault(value, []).append(obj)
    return groups


def count_by(objs, func):
    """Count objects by the passed-in function
    """
    counts = {}
    groups = group_by(objs, func)
    for key, matches in groups.items():
        counts[key] = len(matches)
    return counts


def filter_by(objs, func, expected):
    """Filters the objects by the function passed in
    """
    if not isinstance(expected, (list, tuple)):
        expected = [expected]
    targets = dict([(val, True) for val in expected])

    # group the objects by func value
    groups = group_by(objs, func)

    # purge those that are not in targets
    matches = []
    for key, items in groups.items():
        if not targets.get(key):
            continue
        matches.extend(items)

    # sort them like the original ones
    idxs = list(objs)
    return sorted(matches, key=lambda item: idxs.index(item))


@deprecated("Use filter_by instead")
def filter_by_sample_type(brains, sample_types):
    """Filter to keep samples that have the passed-in sample_types only
    """
    return filter_by(brains, "getSampleTypeTitle", sample_types)


def get_potential_true_pathogen_microorganisms():
    """Returns the potential true pathogens microorganisms that read from csv
    """
    # TODO Cleanup
    microorganisms_file = get_file_resource(
        "potential_true_pathogen_microorganisms.csv"
    )
    microorganisms = read_csv(microorganisms_file)
    pathogen_microorganisms = [
        microorganism.get("Title") for microorganism in microorganisms
        if microorganism.get(
            "Potential true pathogen in blood specimen"
        ) == "Yes"
    ]
    return pathogen_microorganisms


def get_contaminant_microorganisms():
    """Returns the contaminant microorganisms that read from csv
    """
    # TODO Cleanup
    microorganisms_file = get_file_resource(
        "contaminant_microorganisms.csv"
    )
    microorganisms = read_csv(microorganisms_file)
    contaminant_microorganisms = [
        microorganism.get("Title") for microorganism in microorganisms
        if microorganism.get(
            "Probable contaminant in blood specimen"
        ) == "Yes"
    ]
    return contaminant_microorganisms


def is_matched_target_patient(target_patient, sample):
    """Checks whether the sample is match with target patient
    """
    # TODO Cleanup
    bottles = get_field_value(sample, "Bottles")
    container_bottles = [bottle["Container"] for bottle in bottles]
    if (
        TARGET_PATIENTS.getValue(target_patient) == "Adult patient" and
        "Aerobic Blood Bottle" in container_bottles and
        "Anaerobic Blood Bottle" in container_bottles
    ):
        return True
    elif (
        TARGET_PATIENTS.getValue(target_patient) == "Paediatric patient" and
        "Aerobic Blood Bottle" in container_bottles and
        "Anaerobic Blood Bottle" not in container_bottles
    ):
        return True

    return False


def get_target_patient_samples(target_patient, samples):
    """Returns the samples that matched with target patient
    """
    # TODO Cleanup
    target_patient_samples = filter(
        lambda sample: is_matched_target_patient(target_patient, sample),
        samples
    )

    return target_patient_samples


def is_matched_microorganisms_sample(microorganisms, sample):
    """Checks whether the sample contains the microorganisms that in
    target microorganisms list.
    """
    # TODO Cleanup
    # Get the names of the selected microorganisms
    sample_microorganisms = get_identified_microorganisms(sample)
    sample_microorganisms = [api.get_title(m) for m in sample_microorganisms]

    if any(item in microorganisms for item in sample_microorganisms):
        return True
    return False


def get_matched_microorganisms_sample(microorganisms, samples):
    """Returns the samples with growth of potential pathogens
    """
    # TODO Cleanup
    matched_microorganisms_samples = filter(
        lambda sample: is_matched_microorganisms_sample(microorganisms, sample),
        samples
    )

    return matched_microorganisms_samples


def calculate_rate(total_samples, matched_samples):
    """Calculate the rate of matched samples in total samples
    """
    if total_samples > 0:
        rate = round(100 * float(matched_samples) / total_samples, 2)
        return rate
    return 0