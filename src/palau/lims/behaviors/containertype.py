# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

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
