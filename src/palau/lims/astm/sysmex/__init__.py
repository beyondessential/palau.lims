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

from palau.lims.astm import ASTMBaseImporter as Base


class SysmexASTMImporter(Base):
    """Basic ASTM results importer for Sysmex instruments
    """

    def get_sample_id(self, default=None):
        """Get the Sample ID. For Sysmex, the 'sample_id' astm field from
        (O)rder record is not used, but 'instrument specimen id'
        """
        order = self.get_order()
        if not order:
            return default
        instrument = order.get("instrument")
        if not instrument:
            return default
        sid = instrument.get("sample_id").strip()
        if not sid:
            return default
        return sid

    def get_test_id(self, record):
        """Returns the test ID from the given results record
        """
        test = record.get("test") or {}
        param = test.get("parameter") or ""
        return param.strip()
