# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from bes.lims.extender.field import ExtBooleanField
from bes.lims.extender.field import ExtStringField
from bika.lims.interfaces import IClient
from palau.lims import messageFactory as _
from palau.lims.interfaces import IPalauLimsLayer
from Products.Archetypes.Widget import BooleanWidget
from Products.Archetypes.Widget import StringWidget
from zope.component import adapter
from zope.interface import implementer

# New fields to be added to this type
NEW_FIELDS = [

    ExtStringField(
        "Abbreviation",
        mode="rw",
        required=False,
        schemata="default",
        widget=StringWidget(
            label=_("Abbreviation"),
            description=_(
                "The abbreviation of the hospital"
            )
        )
    ),

    ExtBooleanField(
        "WardDepartmentRequired",
        default=False,
        widget=BooleanWidget(
            label=_("Department mandatory"),
            description=_(
                "If enabled, the department in sample form will become a "
                "required field."
            )
        )
    )

]


@adapter(IClient)
@implementer(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
class ClientSchemaExtender(object):
    """Extends Client content type with additional fields
    """
    layer = IPalauLimsLayer

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        default_schemata = schematas["default"]
        idx = default_schemata.index("ClientID")
        abbreviation = default_schemata.pop(
            default_schemata.index("Abbreviation")
        )
        default_schemata.insert(idx + 1, abbreviation)

        schematas["default"] = default_schemata
        return schematas

    def getFields(self):
        return NEW_FIELDS
