# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from bika.lims.interfaces import IContainerType
from palau.lims import messageFactory as _
from palau.lims.content.fields import ExtBooleanField
from palau.lims.interfaces import IPalauLimsLayer
from Products.Archetypes.Widget import BooleanWidget
from zope.component import adapter
from zope.interface import implementer

NEW_FIELDS = [
    ExtBooleanField(
        "BACTECBottle",
        default=False,
        widget=BooleanWidget(
            label=_("BACTEC bottle"),
            description=_(
                "Whether containers from this type are available for selection "
                "when the default container for the selected sample type is a "
                "BACTEC bottle"
            )
        )
    )
]


@adapter(IContainerType)
@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class ContainerTypeSchemaExtender(object):
    """Extends the Container Type with additional fields
    """
    layer = IPalauLimsLayer

    def __init__(self, context):
        self.context = context

    def getFields(self):  # noqa LowerCase
        return NEW_FIELDS
