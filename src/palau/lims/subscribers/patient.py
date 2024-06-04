# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from bika.lims.api import security as sapi
from palau.lims.config import TAMANU_ROLES
from palau.lims.config import TAMANU_USERNAME
from Products.CMFCore.permissions import ModifyPortalContent as modify_perm


def on_patient_added(instance, event):
    """Grant Owner for user 'tamanu' role and revoke ModifyPortalConten
    permission for Patient objects created by user 'tamanu', for all
    users but 'tamanu'.
    """

    # Check if the user is 'tamanu'
    creator = instance.Creator()
    if creator != TAMANU_USERNAME:
        return

    # revoke 'Owner' roles to the creator to prevent further edits
    sapi.revoke_local_roles_for(instance, roles=["Owner"], user=creator)

    # grant 'Owner' role to the user who is modifying the object
    tamanu_user = api.get_user(TAMANU_USERNAME)
    tamanu_user_id = api.user.get_user_id(tamanu_user)
    sapi.grant_local_roles_for(instance, roles=["Owner"], user=tamanu_user_id)

    # don't allow the edition of this object, but Owner only
    sapi.manage_permission_for(instance, modify_perm, ["Owner"], acquire=0)

    instance.reindexObject()
    instance.reindexObjectSecurity()


def on_modified_patient_from_tamanu(instance, event):
    """Grant Owner for user 'tamanu' role and revoke ModifyPortalConten
    permission for Patient objects modified by user 'tamanu', for all
    users but 'tamanu'.
    """

    # Check if the user is 'tamanu'
    if not modified_by_tamanu(instance):
        return

    # revoke 'Owner' roles to the creator to prevent further edits
    creator = instance.Creator()
    if creator != TAMANU_USERNAME:
        sapi.revoke_local_roles_for(instance, roles=TAMANU_ROLES, user=creator)

    # grant 'Owner' role to the user who is modifying the object
    tamanu_user = api.get_user(TAMANU_USERNAME)
    tamanu_user_id = api.user.get_user_id(tamanu_user)
    sapi.grant_local_roles_for(instance, roles=TAMANU_ROLES, user=tamanu_user_id)

    # don't allow the edition of this object, but Owner only
    sapi.manage_permission_for(instance, modify_perm, TAMANU_ROLES, acquire=0)

    instance.reindexObject()
    instance.reindexObjectSecurity()


def modified_by_tamanu(obj):
    """Retrieves True if the object was modified by the user with username
    'tamanu'.
    """
    user = api.get_current_user()
    username = user.getUsername()
    if username == TAMANU_USERNAME:
        return True

    return False
