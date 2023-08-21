# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from AccessControl import ClassSecurityInfo
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from palau.lims import messageFactory as _
from palau.lims.behaviors import get_behavior_schema
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
        self._schema = None

    @property
    def schema(self):
        """Return the schema provided by the underlying behavior
        """
        if self._schema is None:
            behavior = IExtendedSampleContainerBehavior
            behavior_schema = get_behavior_schema(self.context, behavior)
            if not behavior_schema:
                raise TypeError("Not a valid context")
            self._schema = behavior_schema
        return self._schema

    @security.private
    def accessor(self, fieldname):
        """Return the field accessor for the fieldname
        """
        if fieldname not in self.schema:
            return None
        return self.schema[fieldname].get

    @security.private
    def mutator(self, fieldname):
        """Return the field mutator for the fieldname
        """
        if fieldname not in self.schema:
            return None
        return self.schema[fieldname].set

    @security.protected(permissions.View)
    def getWeight(self):
        accessor = self.accessor("weight")
        return accessor(self.context)

    @security.protected(permissions.ModifyPortalContent)
    def setWeight(self, value):
        mutator = self.mutator("weight")
        mutator(self.context, value)

    weight = property(getWeight, setWeight)
