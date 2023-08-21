# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from bika.lims.api import security
from palau.lims.config import UNKNOWN_DOCTOR_FULLNAME
from Products.CMFCore.permissions import ModifyPortalContent


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


def create_unknown_doctor(client):
    """Creates an unknown doctor for the client passed-in
    """
    name = UNKNOWN_DOCTOR_FULLNAME.split(" ")[0]
    surname = UNKNOWN_DOCTOR_FULLNAME[len(name):].strip()
    doctor = api.create(client, "Contact", Firstname=name, Surname=surname)

    # Do not allow the modification of this contact
    roles = security.get_valid_roles_for(doctor)
    security.revoke_permission_for(doctor, ModifyPortalContent, roles)
