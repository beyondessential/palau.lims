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

from palau.lims import messageFactory as _
from palau.lims import utils
from palau.lims.config import UNKNOWN_DOCTOR_FULLNAME
from plone.memoize.instance import memoize
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from senaite.app.listing.utils import add_review_state
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import implements

# Columns to update. List of tuples (column_id, {properties})
UPDATE_COLUMNS = [
    ("Client", {
        "title": _("Location"),
    }),
    ("ClientID", {
        "title": _("Location ID"),
    }),
    ("ClientContact", {
        "title": _("Doctor")
    }),
]

# Columns to remove. List of column ids
REMOVE_COLUMNS = [
]

# Statuses to add. List of dicts
ADD_STATUSES = [
]

# Statuses to update. List of tuples (status_id, {properties})
UPDATE_STATUSES = [
    ("default", {
        "flat_listing": True,
    }),
    ("sample_due", {
        "flat_listing": True,
    }),
    ("sample_received", {
        "flat_listing": True,
    }),
    ("to_be_verified", {
        "flat_listing": True,
    }),
    ("verified", {
        "flat_listing": True,
    })
]


class SamplesListingAdapter(object):
    """Generic adapter for sample listings
    """
    adapts(IListingView)
    implements(IListingViewAdapter)

    # Priority order of this adapter over others
    priority_order = 999999

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    @property
    @memoize
    def senaite_theme(self):
        return getMultiAdapter(
            (self.context, self.listing.request),
            name="senaite_theme")

    def icon_tag(self, name, **kwargs):
        return self.senaite_theme.icon_tag(name, **kwargs)

    def is_unknown_doctor(self, contact_uid):
        """Returns whether contact is an unknown Doctor
        """
        contact = self.listing.get_object_by_uid(contact_uid)
        if contact:
            return contact.getFullname() == UNKNOWN_DOCTOR_FULLNAME
        return False

    def folder_item(self, obj, item, index):
        if self.is_unknown_doctor(obj.getContactUID):
            # Add an icon after the sample ID
            kwargs = {"width": 16, "title": _("Unknown doctor")}
            self.add_icon(item, "getId", "doctor-red", **kwargs)

        # Check if sample has enough volume
        if not utils.is_enough_volume(obj):
            # Add an icon after the sample ID
            kwargs = {"width": 16, "title": _("Not enough sample")}
            self.add_icon(item, "getId", "sample-red", **kwargs)

        return item

    def add_icon(self, item, after_id, icon_name, **kwargs):
        """Adds an icon after the column id
        """
        icon = self.icon_tag(icon_name, **kwargs)
        after_icons = item["after"].get(after_id, "")
        after_icons = "&nbsp;".join([after_icons, icon])
        item["after"].update({after_id: after_icons})

    def before_render(self):
        # Remove columns
        map(lambda c: self.listing.columns.pop(c, None), REMOVE_COLUMNS)

        # Update columns
        for column_id, value in UPDATE_COLUMNS:
            if column_id in self.listing.columns:
                self.listing.columns[column_id].update(value)

        # Add review_states
        for status in ADD_STATUSES:
            after = status.get("after", None)
            before = status.get("before", None)
            if not status.get("columns"):
                status.update({"columns": self.listing.columns.keys()})
            add_review_state(self.listing, status, after=after, before=before)

        # Update review_states
        states_to_update = dict(UPDATE_STATUSES)
        for rv in self.listing.review_states:
            values = states_to_update.get(rv["id"], {})
            rv.update(values)
