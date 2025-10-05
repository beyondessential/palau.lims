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

from AccessControl import ClassSecurityInfo
from palau.lims import messageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFCore import permissions
from senaite.core.interfaces import IContainerType
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


# TODO Port IExtendedContainerTypeBehavior to bes.lims
@provider(IFormFieldProvider)
class IExtendedContainerTypeBehavior(model.Schema):

    bactec_bottle = schema.Bool(
        title=_("BACTEC bottle"),
        description=_(
            "Whether containers from this type are available for selection "
            "when the default container for the selected sample type is a "
            "BACTEC bottle"
        ),
        default=False,
    )


# TODO Port ExtendedContainerType to bes.lims
@implementer(IExtendedContainerTypeBehavior)
@adapter(IContainerType)
class ExtendedContainerType(object):

    security = ClassSecurityInfo()

    def __init__(self, context):
        self.context = context

    @security.protected(permissions.View)
    def getBactecBottle(self):
        accessor = self.context.accessor("bactec_bottle")
        return accessor(self.context)

    @security.protected(permissions.ModifyPortalContent)
    def setBactecBottle(self, value):
        mutator = self.context.mutator("bactec_bottle")
        mutator(self.context, value)

    bactec_bottle = property(getBactecBottle, setBactecBottle)


def getBactecBottle(self):
    behavior = IExtendedContainerTypeBehavior(self)
    return behavior.getBactecBottle()


def setBactecBottle(self, value):
    behavior = IExtendedContainerTypeBehavior(self)
    behavior.setBactecBottle(value)
