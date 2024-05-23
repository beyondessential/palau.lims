# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import six

from plone import api as papi
from Products.CMFCore.permissions import ModifyPortalContent as modify_perm
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.RegistrationTool import get_member_by_login_name
from Products.PlonePAS.tools.memberdata import MemberData

ROLES = ["Owner", ]
TAMANU_USERNAME = 'tamanu'


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

    if user.getUserName() != TAMANU_USERNAME:
        return

    # Ensure creator has Owner role (assuming at least one role)
    papi.user.grant_roles(username=TAMANU_USERNAME, roles=ROLES, obj=instance)

    # Grant Owner role to the Patient object
    instance.manage_permission(modify_perm, roles=(ROLES), acquire=False)

    instance.reindexObject()
    instance.reindexObjectSecurity()


def on_modified_patient_from_tamanu(instance, event):
    """Grant Owner for user 'tamanu' role and revoke ModifyPortalConten
    permission for Patient objects modified by user 'tamanu', for all
    users but 'tamanu'.
    """

    # Check if the user is 'tamanu'
    user = instance.modified_by
    if user.getUserName() != TAMANU_USERNAME:
        return

    # Get portal tools
    portal_membership = getToolByName(instance, 'portal_membership')
    tamanu_user = get_user_by_username(portal_membership, TAMANU_USERNAME)

    # Change creator to 'tamanu' if different
    creator_user = instance.Creator()
    if creator_user != tamanu_user:
        instance.setCreator(TAMANU_USERNAME)

    # Ensure creator has Owner role (assuming at least one role)
    papi.user.grant_roles(username=TAMANU_USERNAME, roles=ROLES, obj=instance)

    # Grant Owner role
    instance.manage_permission(modify_perm, roles=(ROLES), acquire=False)

    instance.reindexObject()
    instance.reindexObjectSecurity()
