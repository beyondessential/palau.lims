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
from palau.lims.utils import to_utf8
from Products.validation.interfaces.IValidator import IValidator
from senaite.core.api import measure as mapi
from zope.interface import implementer


@implementer(IValidator)
class SampleVolumeValidator(object):
    """Verifies the value for Volume field from Sample is valid
    """
    name = "sample_volume_validator"

    def __call__(self, value, *args, **kwargs):
        if not mapi.is_volume(value):
            ts = api.get_tool("translation_service")
            return to_utf8(ts.translate("Not a valid volume"))
