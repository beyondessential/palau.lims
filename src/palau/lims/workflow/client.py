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
from bika.lims.api import security
from palau.lims.config import UNKNOWN_DOCTOR_FULLNAME
from Products.CMFCore.permissions import ModifyPortalContent


# TODO Port client.ObjectCreatedEventHandler to bes.lims
def ObjectCreatedEventHandler(client, event):
    """Actions done when a Client object is created.
    System automatically adds an "Unknown" Contact on creation
    https://github.com/beyondessential/pnghealth.lims/issues/22
    """
    if client.isTemporary():
        # Client is still in the AT creation life-cycle
        return

    # Create a default Contact "Unknown doctor"
    create_unknown_doctor(client)


# TODO Port client.create_unknown_doctor to bes.lims
def create_unknown_doctor(client):
    """Creates an unknown doctor for the client passed-in
    """
    name = UNKNOWN_DOCTOR_FULLNAME.split(" ")[0]
    surname = UNKNOWN_DOCTOR_FULLNAME[len(name):].strip()
    doctor = api.create(client, "Contact", Firstname=name, Surname=surname)

    # Do not allow the modification of this contact
    roles = security.get_valid_roles_for(doctor)
    security.revoke_permission_for(doctor, ModifyPortalContent, roles)
