# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims.api import security
from palau.lims.utils import is_unknown_doctor
from Products.CMFCore.permissions import ModifyPortalContent


def AfterTransitionEventHandler(contact, event):  # noqa camelcase
    """Actions to be done when a transition for a contact takes place.
    If the contact is an Unknown doctor, ensures the contact cannot be modified
    """
    if not event.transition:
        return

    if not is_unknown_doctor(contact):
        return

    # Do not allow the modification of this contact
    roles = security.get_valid_roles_for(contact)
    security.revoke_permission_for(contact, ModifyPortalContent, roles)
