# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims.api.snapshot import get_object_metadata
from palau.lims.config import TAMANU_ROLES
from palau.lims.config import TAMANU_USERNAME
from plone import api as papi
from Products.CMFCore.permissions import ModifyPortalContent as modify_perm


def on_patient_event(instance):
    # Ensure creator has Owner role (assuming at least one role)
    papi.user.grant_roles(
        username=TAMANU_USERNAME, roles=TAMANU_ROLES, obj=instance
    )

    # Grant Owner role to the Patient object
    instance.manage_permission(
        modify_perm, roles=(TAMANU_ROLES), acquire=False
    )

    instance.reindexObject()
    instance.reindexObjectSecurity()


def on_add_patient_from_tamanu(instance, event):
    """Grant Owner for user 'tamanu' role and revoke ModifyPortalConten
    permission for Patient objects created by user 'tamanu', for all
    users but 'tamanu'.
    """

    # Check if the user is 'tamanu'
    if instance.Creator() != TAMANU_USERNAME:
        return

    on_patient_event(instance)


def on_modified_patient_from_tamanu(instance, event):
    """Grant Owner for user 'tamanu' role and revoke ModifyPortalConten
    permission for Patient objects modified by user 'tamanu', for all
    users but 'tamanu'.
    """

    # Check if the user is 'tamanu'
    if not modified_by_tamanu(instance):
        return

    on_patient_event(instance)

    # Revoke permission for creator user
    papi.user.revoke_roles(
        username=instance.Creator(), roles=TAMANU_ROLES, obj=instance
    )


def modified_by_tamanu(obj):
    """Retrieves True if the object was modified by the user with username
    'tamanu'.
    """
    metadata = get_object_metadata(obj)
    if metadata["actor"] == TAMANU_USERNAME:
        return True

    return False
