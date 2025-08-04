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

from bika.lims import api
from bika.lims.interfaces import IAnalysis
from palau.lims.utils import get_field_value
from palau.lims.utils import set_field_value
from senaite.ast.config import REPORT_KEY
from senaite.ast.utils import get_choices
from senaite.ast.utils import get_interim_text


def setGrowthNumber(self, value):  # noqa CamelCase
    """Setter for the GrowthNumber field
    """
    set_field_value(self, "GrowthNumber", value)


def getGrowthNumber(self):  # noqa CamelCase
    """Getter for the GrowthNumber field
    """
    return get_field_value(self, "GrowthNumber")


def setInterimFields(self, value):  # noqa CamelCase
    """Setter for interim fields that ensures a default 'N' for AST-reporting
    analyses
    """
    value = value or []
    if IAnalysis.providedBy(self) and self.getKeyword() == REPORT_KEY:
        # Default to 'N' if no value is set
        for interim in value:
            text_value = get_interim_text(interim, default="")
            if not text_value:
                choices = get_choices(interim)
                choices = dict(map(lambda ch: (ch[1], ch[0]), choices))
                interim.update({"value": choices.get("N", "")})

    self.getField("InterimFields").set(self, value)
