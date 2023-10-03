# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import collections

from bika.lims import api
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from zope.component import adapter
from zope.interface import implementer
from palau.lims import messageFactory as _


@adapter(IListingView)
@implementer(IListingViewAdapter)
class SampleAnalysesListingAdapter(object):
    """Adapter for analyses listings
    """

    # Priority order of this adapter over others
    priority_order = 99999

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def folder_item(self, obj, item, index):
        self.render_results_range(obj, item)
        return item

    def render_results_range(self, obj, item):
        """Sets the results range to the item passed in
        """
        analysis = self.listing.get_object(obj)

        # use listing's default if value for min or max or both
        specs = analysis.getResultsRange()
        range_min = api.to_float(specs.get("min"), default=0)
        range_max = api.to_float(specs.get("max"), default=0)
        if any([range_min, range_max]):
            return

        # no value set for neither min nor max, show the range comment
        comment = specs.get("rangecomment")
        if comment:
            item["replace"]["Specification"] = comment

    def before_render(self):
        # Move "Analyst" and "Status" columns to the end, before "Due date"
        self.move_column("Analyst", before="DueDate")
        self.move_column("state_title", after="Analyst")

        # Rename the column "Specification" to "Normal values"
        for key, value in self.listing.columns.items():
            if key == "Specification":
                value["title"] = _(
                    u"title_column_specification_analyses",
                    default=u"Normal value")

    def move_column(self, column_id, before=None, after=None):
        """Moves the column with the id passed in to the new position
        """
        column = self.listing.columns.pop(column_id)
        out_columns = collections.OrderedDict()
        for key, item in self.listing.columns.items():
            if before == key:
                out_columns[column_id] = column
            out_columns[key] = item
            if after == key:
                out_columns[column_id] = column
        self.listing.columns = out_columns

        for state in self.listing.review_states:
            rv_state = state.copy()
            cols = rv_state.get("columns", [])
            if column_id not in cols:
                continue
            cols.remove(column_id)
            idx = len(cols)
            if before in cols:
                idx = cols.index(before)
            elif after in cols:
                idx = cols.index(after) + 1

            cols.insert(idx, column_id)
