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

import logging

from palau.lims import permissions
from Products.Archetypes.atapi import listTypes
from Products.Archetypes.atapi import process_types
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.utils import ContentInit
from zope.i18nmessageid import MessageFactory

PRODUCT_NAME = "palau.lims"
PROFILE_ID = "profile-{}:default".format(PRODUCT_NAME)

# Defining a Message Factory for when this product is internationalized.
messageFactory = MessageFactory(PRODUCT_NAME)

logger = logging.getLogger(PRODUCT_NAME)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    logger.info("*** Initializing PALAU LIMS Customization package ***")

    # Get the content types from this product
    types = listTypes(PRODUCT_NAME)
    content_types, constructors, ftis = process_types(types, PRODUCT_NAME)

    # Register each type with it's own Add permission
    # use "Add portal content" as default
    all_types = zip(content_types, constructors)
    for content_type, constructor in all_types:
        kind = "%s: Add %s" % (PRODUCT_NAME, content_type.portal_type)
        perm_name = "Add{}".format(content_type.portal_type)
        perm = getattr(permissions, perm_name, AddPortalContent)
        ContentInit(kind,
                    content_types=(content_type,),
                    permission=perm,
                    extra_constructors=(constructor, ),
                    fti=ftis,
                    ).initialize(context)
