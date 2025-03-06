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

from palau.lims.utils import is_growth_editable
from senaite.ast.datamanagers import ASTAnalysisDataManager


def is_field_writeable(self, field):
    if field.getName() == "GrowthNumber":
        # GrowthNumber field applies to multiple analyses for same
        # microorganism, so even if an analysis is already verified, user
        # should be able to modify the value if there is one sibling in a
        # suitable status
        return is_growth_editable(self.context)

    return super(ASTAnalysisDataManager, self).is_field_writeable(field)
