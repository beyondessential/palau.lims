# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


def disable_csfr(site, event):
    """Disables the CSFR protection
    """
    request = api.get_request()
    alsoProvides(request, IDisableCSRFProtection)
