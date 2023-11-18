# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd


from bika.lims import api
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from senaite.app.listing.utils import add_column
from senaite.patient import messageFactory as _p
from zope.component import adapter
from zope.interface import implementer

# Columns to remove. List of column ids
REMOVE_COLUMNS = [
]

# Columns to add
ADD_COLUMNS = [
    ("Patient", {
        "title": _p("Patient"),
        "sortable": False,
        "after": "Batch",
    }),
    ("MRN", {
        "title": _p("MRN"),
        "sortable": True,
        "index": "medical_record_number",
        "after": "Batch",
    }),
]

# Columns to update. List of tuples (column_id, {properties})
UPDATE_COLUMNS = [
]


@adapter(IListingView)
@implementer(IListingViewAdapter)
class ReportsListingAdapter(object):
    """Adapter for reports listings
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
        report = api.get_object(obj)
        sample = report.getAnalysisRequest()
        item["MRN"] = sample.getMedicalRecordNumberValue()
        item["Patient"] = sample.getPatientFullName()
