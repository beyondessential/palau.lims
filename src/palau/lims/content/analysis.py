# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS.
#
# PALAU.LIMS is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2023-2025 by it's authors.
# Some rights reserved, see README and LICENSE.

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
