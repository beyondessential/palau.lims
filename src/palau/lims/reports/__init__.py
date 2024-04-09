# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

import re

from datetime import datetime

from bika.lims import api
from senaite.core.api import dtime
from senaite.core.catalog import ANALYSIS_CATALOG
from senaite.core.catalog import SAMPLE_CATALOG
from senaite.core.catalog import SETUP_CATALOG


INT_RE = re.compile(r"\d+")

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

        elif not value and value != 0:
            # handle Missing.Value properly
            value = None

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


def get_analyses(from_date, to_date, **kwargs):
    """Returns the analyses that were received within the passed-in date range
    """
    query = {
        "portal_type": "Analysis",
        "getDateReceived": {
            "query": [from_date, to_date],
            "range": "min:max"
        },
        "sort_on": "getDateReceived",
        "sort_order": "ascending",
    }
    query.update(**kwargs)
    return api.search(query, ANALYSIS_CATALOG)


def get_analyses_by_year(year, **kwargs):
    """Returns the analyses received within the passed-in year
    """
    from_date = dtime.date_to_string(datetime(year, 1, 1))
    to_date = dtime.date_to_string(datetime(year, 12, 31))
    return get_analyses(from_date, to_date, **kwargs)


def get_analyses_by_result_category_department(resultText, category, department, **kwargs):  # noqa
    """Returns the analyses filtering by the result
    """
    analyses_result_filtered = []
    query = {
        "portal_type": "Analysis",
    }

    # if resultText:
    #     query["getResultOptions"] = {
    #         "query": {
    #             "ResultText": {
    #                 "query": resultText
    #             }
    #         }
    #     }

    if category:
        query["getCategoryTitle"] = {"query": category}
    if department:
        department_query = {
            "portal_type": "Department",
            "Title": department
        }
        department_brain = api.search(department_query, SETUP_CATALOG)[0]
        department_obj = api.get_object(department_brain)
        department_uid = department_obj.getDepartmentID()

        query["getDepartment"] = {"query": department_uid}

    query.update(**kwargs)

    brains = api.search(query, ANALYSIS_CATALOG)
    if not brains:
        return analyses_result_filtered

    objs = map(api.get_object, brains)

    if not resultText:
        return objs

    for analysis in objs:
        for option in analysis.getResultOptions():
            result_matches = INT_RE.search(analysis.getResult())
            result = result_matches.group(0) if result_matches else ''

            if option["ResultText"] == resultText and option["ResultValue"] == result:
                analyses_result_filtered.append(analysis)
                break
                
    return analyses_result_filtered
