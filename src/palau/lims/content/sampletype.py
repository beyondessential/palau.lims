# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.interfaces import ISampleType
from palau.lims import messageFactory as _
from palau.lims.content import update_field
from palau.lims.content.fields import ExtStringField
from palau.lims.content.fields import ExtTextField
from palau.lims.interfaces import IPalauLimsLayer
from Products.Archetypes import DisplayList
from Products.Archetypes.Widget import RichWidget
from Products.Archetypes.Widget import SelectionWidget
from Products.Archetypes.Widget import StringWidget
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import View
from zope.component import adapts
from zope.interface import implementer

# Display list with the types of widget to be rendered on Sample add form and
# Sample view when this Sample Type is selected
# https://github.com/beyondessential/pnghealth.lims/issues/28
CONTAINER_WIDGET_TYPES = DisplayList((
    ("container", _("Generic search control")),
    ("bottles", _("BACTEC bottles control")),
))


# A tuple with (field_name, properties), where properties is a dict
UPDATED_FIELDS = [
    ("MinimumVolume", {
        "required": False,
    }),
]


# New fields to be added to this type
NEW_FIELDS = [
    ExtStringField(
        "ContainerWidget",
        vocabulary=CONTAINER_WIDGET_TYPES,
        required=False,
        default="container",
        read_permission=View,
        write_permission=ModifyPortalContent,
        widget=SelectionWidget(
            label=_("Widget for container selection"),
            description=_(
                "Widget to display on sample view and add sample form for the "
                "selection of the sample container when this sample type is "
                "selected."
            ),
            format="select",
        ),
    ),
    ExtTextField(
        "InsufficientVolumeText",
        read_permission=View,
        write_permission=ModifyPortalContent,
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
    ),
    ExtStringField(
        "MaximumVolume",
        required=True,
        widget=StringWidget(
            label=_("Maximum Volume"),
            description=_(
                "The maximum sample volume required for analysis "
                "eg. '10 ml' or '1 kg'."),
        ),
    ),

]

# Fields order. A list of tuples of (fieldname, schemata, after)
FIELDS_ORDER = [
    ("MaximumVolume", "default", "MinimumVolume")
]

@implementer(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
class SampleTypeSchemaExtender(object):
    """Extends Sample Type content type with additional fields
    """
    adapts(ISampleType)
    layer = IPalauLimsLayer

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        for field_name, sch_id, after in FIELDS_ORDER:
            sch = schematas[sch_id]
            idx = sch.index(after)
            del (sch[sch.index(field_name)])
            sch.insert(idx + 1, field_name)
        return schematas

    def getFields(self):
        return NEW_FIELDS


@implementer(ISchemaModifier, IBrowserLayerAwareExtender)
class SampleTypeSchemaModifier(object):
    adapts(ISampleType)
    layer = IPalauLimsLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        # Update some fields (title, description, etc.)
        map(lambda f: update_field(schema, f[0], f[1]), UPDATED_FIELDS)

        return schema
