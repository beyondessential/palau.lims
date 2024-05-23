# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import six

from Products.CMFCore.permissions import ModifyPortalContent as modify_perm
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.RegistrationTool import get_member_by_login_name
from Products.PlonePAS.tools.memberdata import MemberData


def get_user_by_username(portal_membership, username):
    """Retrieves a user object based on username.
    """
    """Return Plone User
    """
    user = None
    if isinstance(username, MemberData):
        user = username
    if isinstance(username, six.string_types):
        user = get_member_by_login_name(portal_membership, username, False)
    return user


def on_add_patient_from_tamanu(instance, event):
    """Grant Owner for user 'tamanu' role and revoke ModifyPortalConten
    permission for Patient objects created by user 'tamanu', for all
    users but 'tamanu'.
    """

    # Check if the user is 'tamanu'
    username = instance.Creator()
    portal_membership = getToolByName(instance, 'portal_membership')
    user = get_user_by_username(portal_membership, username)
    if user.getUserName() != 'tamanu':
        return

    # Ensure creator has Owner role (assuming at least one role)
    owner_role = portal_membership.getAuthenticatedMember().getRoles()[0]
    if owner_role not in user.getRoles():
        user.setRoles(owner_role)

    # Grant Owner role to the Patient object
    instance.manage_permission(modify_perm, roles=(owner_role), acquire=False)
    instance.reindexObject()


def on_modified_patient_from_tamanu(instance, event):
    """GGrant Owner for user 'tamanu' role and revoke ModifyPortalConten
    permission for Patient objects modified by user 'tamanu', for all
    users but 'tamanu'.
    """

    # Check if the user is 'tamanu'
    user = instance.modified_by
    if user.getUserName() != 'tamanu':
        return

    # Get portal tools
    portal_membership = getToolByName(instance, 'portal_membership')
    tamanu_user = get_user_by_username(portal_membership, 'tamanu')

    # Change creator to 'tamanu' if different
    creator_user = instance.Creator()
    if creator_user != tamanu_user:
        instance.manage_permission(
            'Creator', roles=[tamanu_user.getId()], acquire=False
        )

    # Ensure creator has Owner role (assuming at least one role)
    owner_role = portal_membership.getAuthenticatedMember().getRoles()[0]
    if owner_role not in creator_user.getRoles():
        creator_user.serRoles(owner_role)

    # Grant Owner role
    instance.manage_permission(modify_perm, roles=(owner_role), acquire=False)
    instance.reindexObject()
