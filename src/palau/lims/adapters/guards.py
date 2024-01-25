# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from bika.lims.interfaces import IGuardAdapter
from palau.lims.utils import is_unknown_doctor
from zope.interface import implements


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

    def guard_set_out_of_stock(self):
        """Returns true if the patient state is unassigned or assigned
        """
        return self.context.review_states in ["unassigned", "assigned"]
