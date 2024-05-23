# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from Products.CMFCore.utils import getToolByName
from zope.lifecycleevent import Attributes


def on_add_patient_from_tamanu(instance, event):
    """Grant Owner role and revoke ModifyPortalContent permission
    for Patient objects created by user 'tamanu'.

    Args:
        instance: The Patient object being added.
        event: The IObjectAddedEvent instance.
    """

    # Check if the user is 'tamanu'
    user = event.getObject().creator
    if user.getUserName() != 'tamanu':
        return

    # Get portal_membership and permission mapping tools
    portal_membership = getToolByName(instance, 'portal_membership')
    portal_permissions = getToolByName(instance, 'portal_permissions')

    # Grant Owner role - assuming 'tamanu' has at least one role
    owner_role = portal_membership.getAuthenticatedMember().getRoles()[0]
    instance.manage_permission(owner_role, roles=[owner_role], acquire=False)

    # Revoke ModifyPortalContent permission for all except Owner
    perms_mapping = portal_permissions.getPermission('ModifyPortalContent')
    mapping = perms_mapping.getMapping()

    for role in mapping.keys():
        if role != owner_role:
            mapping[role] = Attributes(
                                acquired=False, inherited=False, value=0
                            )

    perms_mapping.setMapping(mapping)


def on_modified_patient_from_tamanu(instance, event):
    """Grant Owner role and revoke ModifyPortalContent permission
    for Patient objects modified by user 'tamanu'.

    This function behaves similarly to on_add_patient_from_tamanu
    but checks for modification events.

    Args:
        instance: The Patient object being modified.
        event: The IObjectModifiedEvent instance.
    """

    # Similar logic as on_add_patient_from_tamanu, checking user and tools
    user = event.object.modified_by
    if user.getUserName() != 'tamanu':
        return

    portal_membership = getToolByName(instance, 'portal_membership')
    portal_perms = getToolByName(instance, 'portal_permissions')

    # Grant Owner role
    owner_role = portal_membership.getAuthenticatedMember().getRoles()[0]
    instance.manage_permission(owner_role, roles=[owner_role], acquire=False)

    # Revoke ModifyPortalContent permission for all except Owner
    permission_mapping = portal_perms.getPermission('ModifyPortalContent')
    mapping = permission_mapping.getMapping()

    for role in mapping.keys():
        if role != owner_role:
            mapping[role] = Attributes(
                    acquired=False, inherited=False, value=0
                )

    permission_mapping.setMapping(mapping)
