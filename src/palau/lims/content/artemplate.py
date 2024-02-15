# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims import senaiteMessageFactory as _c
from bika.lims.interfaces import IARTemplate
from palau.lims import messageFactory as _
from palau.lims.content import disable_field
from palau.lims.content import update_field
from palau.lims.content.fields import ExtStringField
from palau.lims.content.fields import ExtTextField
from palau.lims.interfaces import IPalauLimsLayer
from palau.lims.validators import SampleVolumeValidator
from Products.Archetypes.public import StringWidget
from Products.Archetypes.Widget import RichWidget
from Products.CMFCore import permissions
from zope.component import adapts
from zope.interface import implementer

# A list with the names of the fields to be disabled
DISABLED_FIELDS = [
    "Remarks",
]

# A tuple with (fieldname, properties), where properties is a dict
UPDATED_FIELDS = [
]

# A list of new fields to be added in the Schema
NEW_FIELDS = [
    ExtStringField(
        "MinimumVolume",
        validators=SampleVolumeValidator(),
        widget=StringWidget(
            label=_c("Minimum volume"),
            description=_c(
                "The minimum sample volume required for analysis eg. '10 ml')"),  # noqa
        )
    ),
    ExtTextField(
        "InsufficientVolumeText",
        read_permission=permissions.View,
        write_permission=permissions.ModifyPortalContent,
        default_content_type='text/html',
        default_output_type='text/x-html-safe',
        widget=RichWidget(
            label=_("Auto-text for when there is not enough volume"),
            description=_(
                "When there is not enough volume, the contents entered here "
                "are automatically inserted in Results Interpretation after "
                "Sample verification"
            ),
            default_mime_type='text/x-rst',
            output_mime_type='text/x-html',
            allow_file_upload=False,
            rows=10,
        )
    )
]

# Fields order. A list of tuples of (fieldname, schemata, after)
FIELDS_ORDER = [
    ("MinimumVolume", "default", "SampleType")
]


@implementer(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
class ARTemplateSchemaExtender(object):
    """Extends the ARTemplate with additional fields
    """
    adapts(IARTemplate)
    layer = IPalauLimsLayer

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):  # noqa LowerCase
        for field_name, sch_id, after in FIELDS_ORDER:
            sch = schematas[sch_id]
            idx = sch.index(after)
            del(sch[sch.index(field_name)])
            sch.insert(idx + 1, field_name)
        return schematas

    def getFields(self):  # noqa LowerCase
        return NEW_FIELDS


@implementer(ISchemaModifier, IBrowserLayerAwareExtender)
class ARTemplateSchemaModifier(object):
    adapts(IARTemplate)
    layer = IPalauLimsLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        # Disable some of the fields
        map(lambda f: disable_field(schema, f), DISABLED_FIELDS)

        # Update some fields (title, description, etc.)
        map(lambda f: update_field(schema, f[0], f[1]), UPDATED_FIELDS)

        return schema
