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

from palau.lims.astm.sysmex import SysmexASTMImporter
from senaite.core.interfaces import IASTMImporter
from senaite.core.interfaces import ISenaiteCore
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


KEYWORDS_MAPPING = (
    # Tuple of (instrument_parameter, (service_keywords))
    ("HCT", ["HCT"]),
    ("HGB", ["Hb-"]),
    ("LYM#", ["LYMPH"]),
    ("LYM%", ["Lymphocytes"]),
    ("MCH", ["MCH"]),
    ("MCHC", ["MCHC"]),
    ("MCV", ["MCV"]),
    ("MPV", ["MPV"]),
    ("NEUT#", ["NEUT"]),
    ("NEUT%", ["Neutrophils"]),
    ("RBC", ["RBC_BF", "Red-CC", "RBC", "RPBC"]),
    ("WBC", ["WBC_BF", "White-CC", "WBC", "PWBC", "WC"]),
    ("MXD%", ["MXD"]),
    ("MXD#", ["MXDA"]),
)


@adapter(Interface, Interface, ISenaiteCore)
@implementer(IASTMImporter)
class ASTMImporter(SysmexASTMImporter):
    """ASTM results importer for Sysmex XP-100
    """

    @property
    def keywords_mapping(self):
        return dict(KEYWORDS_MAPPING)
