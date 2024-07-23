# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from AccessControl import ClassSecurityInfo
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from palau.lims import messageFactory as _
from Products.CMFCore import permissions
from senaite.core.interfaces import ISampleContainer
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IExtendedSampleContainerBehavior(model.Schema):

    weight = schema.TextLine(
        title=_(u"Weight"),
        description=_(
            u"Dry weight of the container. When set, the volume of the "
            u"sample is calculated automatically by subtracting this value "
            u"from the container's weight set on sample registration"
        ),
        default=u"0 ml",
    )


@implementer(IExtendedSampleContainerBehavior)
@adapter(ISampleContainer)
class ExtendedSampleContainer(object):

    security = ClassSecurityInfo()

    def __init__(self, context):
        self.context = context

    @security.protected(permissions.View)
    def getWeight(self):
        accessor = self.context.accessor("weight")
        return accessor(self.context)

    @security.protected(permissions.ModifyPortalContent)
    def setWeight(self, value):
        mutator = self.context.mutator("weight")
        mutator(self.context, value)

    weight = property(getWeight, setWeight)


def getWeight(self):
    behavior = IExtendedSampleContainerBehavior(self)
    return behavior.getWeight()


def setWeight(self, value):
    behavior = IExtendedSampleContainerBehavior(self)
    behavior.setWeight(value)
