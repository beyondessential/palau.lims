# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from zope.component import adapter
from zope.interface import implementer
from palau.lims import messageFactory as _
from bika.lims import api


@adapter(IListingView)
@implementer(IListingViewAdapter)
class ClientsListingAdapter(object):
    """Adapter for clients listings
    """

    # Priority order of this adapter over others
    priority = 1000

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        self.listing.columns["Abbreviation"] = {
            "title": _("Abbreviation"),
            "toggle": True
        }

        for rv in self.listing.review_states:
            rv["columns"] = self.listing.columns.keys()

    def folder_item(self, obj, item, index):
        obj = api.get_object(obj)
        abbreviation = obj.getField("Abbreviation").get(obj) or ""
        item["Abbreviation"] = abbreviation
        return item
