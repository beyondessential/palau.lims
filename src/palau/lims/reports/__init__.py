# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

import itertools
from bika.lims import api
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


def get_percentage(num, total, ndigits=2):
    """Returns the percentage rate of num from the total
    """
    rate = 0.0
    if all([num, total]):
        rate = float(num) / total
    return round(100 * rate, ndigits)


def is_reportable(analysis):
    hidden = analysis.getHidden()
    if hidden:
        return False

    reportable = ["verified", "published"]
    return api.get_review_status(analysis) in reportable


def get_reportable_analyses(samples):
    """Returns the samples that matched with target patient
    """
    samples_analyses = []
    for sample in samples:
        analyses = sample.getAnalyses()
        analyses = map(api.get_object, analyses)
        samples_analyses.append(analyses)
    samples_analyses = list(itertools.chain.from_iterable(samples_analyses))
    reportable_analyses = filter(is_reportable, samples_analyses)
    return reportable_analyses
