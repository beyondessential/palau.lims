# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from bika.lims.interfaces import IAnalysisProfile
from palau.lims import messageFactory as _
from palau.lims.content.fields import ExtUIDReferenceField
from palau.lims.interfaces import IPalauLimsLayer
from senaite.core.browser.widgets import ReferenceWidget
from senaite.core.catalog import SETUP_CATALOG
from zope.component import adapts
from zope.interface import implementer


# A list of new fields to be added in the Schema
NEW_FIELDS = [
    ExtUIDReferenceField(
        "SampleTypes",
        allowed_types=("SampleType", ),
        multiValued=True,
        widget=ReferenceWidget(
            label=_(
                "label_analysisprofile_sampletypes",
                default="Sample types"
            ),
            description=_(
                "description_analysisprofile_sampletypes",
                default="Sample types for which this analysis profile is"
                        "supported."
            ),
            catalog_name=SETUP_CATALOG,
            base_query={'is_active': True,
                        "sort_on": "sortable_title",
                        "sort_order": "ascending"},
            showOn=True,
        )
    ),
]

# Fields order. A list of tuples of (fieldname, schemata, after)
FIELDS_ORDER = [
    ("SampleTypes", "default", "ProfileKey")
]


@implementer(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
class AnalysisProfileSchemaExtender(object):
    """Extends the Analysis Profile with additional fields
    """
    adapts(IAnalysisProfile)
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
