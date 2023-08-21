# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

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
