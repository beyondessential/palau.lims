# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from bika.lims.interfaces import IBikaSetup
from palau.lims import messageFactory as _
from palau.lims.content.fields import ExtBlobImageField
from palau.lims.interfaces import IPalauLimsLayer
from Products.Archetypes.Widget import ImageWidget
from zope.component import adapter
from zope.interface import implementer

# New fields to be added to this type
NEW_FIELDS = [

    ExtBlobImageField(
        "ReportLogo",
        schemata="Results Reports",
        widget=ImageWidget(
            label=_("Report Logo"),
            description=_(
                "Logo to display in the header of results reports"
            )
        ),
    ),

]


@adapter(IBikaSetup)
@implementer(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
class LimsSetupSchemaExtender(object):
    """Extends Setup content type with additional fields
    """
    layer = IPalauLimsLayer

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return NEW_FIELDS
