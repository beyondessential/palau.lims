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
from bika.lims.interfaces import IBikaSetup
from palau.lims.content import disable_field
from palau.lims.interfaces import IPalauLimsLayer
from zope.component import adapter
from zope.interface import implementer

# field names to disable
DISABLED_FIELDS = (
    "SamplingWorkflowEnabled",
    "ScheduleSamplingEnabled",
)


@adapter(IBikaSetup)
@implementer(ISchemaModifier, IBrowserLayerAwareExtender)
class BikaSetupSchemaModifier(object):
    """Modifies the existing schema of BikaSetup"""

    layer = IPalauLimsLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        map(lambda f: disable_field(schema, f), DISABLED_FIELDS)
        return schema
