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

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims import senaiteMessageFactory as _c
from bika.lims.interfaces import IBaseAnalysis
from palau.lims import messageFactory as _
from palau.lims.content import update_field
from palau.lims.interfaces import IPalauLimsLayer
from Products.Archetypes import DisplayList
from zope.component import adapter
from zope.interface import implementer


# A tuple with (field_name, properties), where properties is a dict
UPDATED_FIELDS = [
    ("ResultOptions", {
        "subfields": ("ResultValue", "ResultText", "Flag"),
        "subfield_labels": {
            "ResultValue": _c("Result Value"),
            "ResultText": _c("Display Value"),
            "Flag": _("Flag"),
        },
        "subfield_types": {
            "Flag": "selection",
        },
        "subfield_sizes": {
            "Flag": 1,
        },
        "subfield_vocabularies": {
            "Flag": DisplayList((
                ('', ''),
                ('negative', _('Negative')),
                ('positive', _('Positive')),
            )),
        },
    }),
]


@adapter(IBaseAnalysis)
@implementer(ISchemaModifier, IBrowserLayerAwareExtender)
class BaseAnalysisSchemaModifier(object):
    layer = IPalauLimsLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        # Update some fields (title, description, etc.)
        map(lambda f: update_field(schema, f[0], f[1]), UPDATED_FIELDS)
        return schema
