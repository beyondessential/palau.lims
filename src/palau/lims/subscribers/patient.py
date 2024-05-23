# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from palau.lims.config import TAMANU_ROLES
from palau.lims.config import TAMANU_USERNAME
from Products.CMFCore.permissions import ModifyPortalContent as modify_perm
from zope.component import getSiteManager
from zope.lifecycleevent import IObjectModifiedEvent


def on_patient_event(instance):
    # Ensure creator has Owner role (assuming at least one role)
    papi.user.grant_roles(username=TAMANU_USERNAME, roles=TAMANU_ROLES, obj=instance)

    # Grant Owner role to the Patient object
    instance.manage_permission(modify_perm, roles=(TAMANU_ROLES), acquire=False)

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
    if get_latest_modifier_username(instance) != TAMANU_USERNAME:
        return

    # Change creator to 'tamanu' if different
    if instance.Creator() != TAMANU_USERNAME:
        instance.setCreator(TAMANU_USERNAME)

    on_patient_event(instance)


def get_latest_modifier_username(obj):
    """Retrieves the username of the last person who modified the given object.
    """
    sm = getSiteManager()
    events = sm.adapters.subscribers((obj,), IObjectModifiedEvent)

    if events:
        latest_event = events[-1]
        modifier_user = latest_event.user
        if modifier_user:
            return modifier_user.getUserName()

    return None
