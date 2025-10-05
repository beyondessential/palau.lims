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

from bika.lims import api
from bika.lims.interfaces import IGuardAdapter
from palau.lims.utils import is_unknown_doctor
from zope.interface import implements


# TODO Port SampleGuardAdapter to bes.lims
class SampleGuardAdapter(object):
    implements(IGuardAdapter)

    def __init__(self, context):
        self.context = context

    def guard(self, action):
        func_name = "guard_{}".format(action)
        func = getattr(self, func_name, None)
        if func:
            return func()

        # No guard intercept here
        return True

    def guard_reject(self):
        """Returns true if the lab contact linked to the current user has
        the option 'Can reject samples' selected
        """
        # Get the contact this user is linked to, if any
        user = api.get_current_user()
        contact = api.get_user_contact(user, contact_types=["LabContact"])
        if contact:
            return contact.getField("AuthorisedRejection").get(contact)

        # Directly rely on the built-in guard
        return True

    def guard_verify(self):
        """Returns true if the doctor set is not unknown
        """
        contact = self.context.getContact()
        if not contact or is_unknown_doctor(contact):
            return False

        return True
