# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims.api import security as sapi
from bika.lims.api import user as uapi
from palau.lims.config import TAMANU_ID
from Products.CMFCore.permissions import ModifyPortalContent


def on_patient_added(instance, event):
    """Grant Owner for user 'tamanu' role and revoke ModifyPortalContent
    permission for Patient objects created by user 'tamanu', for all
    users but 'tamanu'.
    """
    if uapi.get_user_id() != TAMANU_ID:
        # user creating the patient is not tamanu's, do nothing
        return

    # don't allow the edition, but to tamanu (Owner) only
    sapi.manage_permission_for(instance, ModifyPortalContent, ["Owner"])

    # re-index object security indexes (e.g. allowedRolesAndUsers)
    instance.reindexObjectSecurity()


def on_patient_modified(instance, event):
    """Grant Owner for user 'tamanu' role and revoke ModifyPortalContent
    permission for Patient objects modified by user 'tamanu', for all
    users but 'tamanu'.
    """
    user_id = uapi.get_user_id()
    if user_id != TAMANU_ID:
        # user modifying the patient is not tamanu's, do nothing
        return

    # revoke 'Owner' roles to the creator to prevent further edits
    creator = instance.Creator()
    if creator != TAMANU_ID:
        sapi.revoke_local_roles_for(instance, roles=["Owner"], user=creator)

    # grant 'Owner' role to the user who is modifying the object
    sapi.grant_local_roles_for(instance, roles=["Owner"], user=user_id)

    # don't allow the edition, but to tamanu (Owner) only
    sapi.manage_permission_for(instance, ModifyPortalContent, ["Owner"])

    # re-index object security indexes (e.g. allowedRolesAndUsers)
    instance.reindexObjectSecurity()
