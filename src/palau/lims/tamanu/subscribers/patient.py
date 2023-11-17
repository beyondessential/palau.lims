# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from bika.lims.api import security
from Products.CMFCore.permissions import ModifyPortalContent


def modifiedPatient(obj, event):
    """Patient was modified, cloned or created
    """
    username = api.get_current_user().id
    if username == "tamanu":
        security.grant_local_roles_for(obj, "Owner", username)
        roles = security.get_valid_roles_for(obj)
        security.revoke_permission_for(obj, ModifyPortalContent, roles)
        obj.reindexObject()
