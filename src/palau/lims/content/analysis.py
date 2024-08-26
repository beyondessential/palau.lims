# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import copy

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from bes.lims.extender.field import ExtIntegerField
from bika.lims.interfaces import IAnalysis
from bika.lims.interfaces.analysis import IRequestAnalysis
from palau.lims.interfaces import IPalauLimsLayer
from senaite.ast.utils import get_ast_siblings
from zope.component import adapter
from zope.interface import implementer


class GrowthNumberField(ExtIntegerField):
    """Field extender of IntegerField that stores the GrowthNumber in analysis
    """
    def set(self, instance, value, **kwargs):
        super(GrowthNumberField, self).set(instance, value, **kwargs)

        # Do not do anything while initializing the field
        if kwargs.get("_initializing_", False):
            return

        # Do not do anything unless the instance is from a Sample
        if not IRequestAnalysis.providedBy(instance):
            return

        # Maybe a duplicate is being created, with no analysis assigned yet
        if not instance.getRequest():
            return

        # Update the value of growth number field for the rest of AST-analyses
        # for same microorganism, but only if the instance is an analysis
        field_name = self.getName()
        for analysis in get_ast_siblings(instance):
            field = analysis.getField(field_name)
            if field.get(analysis) != value:
                nargs = copy.deepcopy(kwargs)
                nargs["_initializing_"] = True
                field.set(analysis, value, **nargs)


NEW_FIELDS = [
    GrowthNumberField(
        "GrowthNumber",
    )
]


@adapter(IAnalysis)
@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class AnalysisSchemaExtender(object):
    """Extends the Analysis with additional fields
    """
    layer = IPalauLimsLayer

    def __init__(self, context):
        self.context = context

    def getFields(self):  # noqa LowerCase
        return NEW_FIELDS
