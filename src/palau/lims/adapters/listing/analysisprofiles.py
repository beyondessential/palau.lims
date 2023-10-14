# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd


from bika.lims import api
from palau.lims import messageFactory as _
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from senaite.app.listing.utils import add_column
from zope.component import adapter
from zope.interface import implementer
from bika.lims.utils import get_link_for


# Columns to remove. List of column ids
REMOVE_COLUMNS = [
]

# Columns to add
ADD_COLUMNS = [
    ("SampleTypes", {
        "title": _(
            "column_analysisprofiles_sampletypes",
            default="Sample types",
        ),
        "index": "sampletype_title",
        "sortable": True,
        "after": "ProfileKey",
    }),
]

# Columns to update. List of tuples (column_id, {properties})
UPDATE_COLUMNS = [
]


@adapter(IListingView)
@implementer(IListingViewAdapter)
class AnalysisProfilesListingAdapter(object):
    """Adapter for analysis profiles listings
    """

    # Priority order of this adapter over others
    priority = 1000

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        # Remove columns
        map(lambda c: self.listing.columns.pop(c, None), REMOVE_COLUMNS)

        # Add columns
        rv_keys = map(lambda r: r["id"], self.listing.review_states)
        for column_id, column_values in ADD_COLUMNS:
            add_column(
                listing=self.listing,
                column_id=column_id,
                column_values=column_values,
                after=column_values.get("after", None),
                review_states=rv_keys)

        # Update columns
        for column_id, value in UPDATE_COLUMNS:
            if column_id in self.listing.columns:
                self.listing.columns[column_id].update(value)

    def folder_item(self, obj, item, index):
        obj = api.get_object(obj)
        item["SampleTypes"] = obj.getRawSampleTypes()

        links = map(get_link_for, obj.getSampleTypes())
        item["replace"]["SampleTypes"] = ", ".join(links)
        return item
