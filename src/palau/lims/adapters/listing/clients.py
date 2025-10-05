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

from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from zope.component import adapter
from zope.interface import implementer
from palau.lims import messageFactory as _
from bika.lims import api


# TODO Port ClientsListingAdapter to bes.lims
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
