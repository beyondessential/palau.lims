# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

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
