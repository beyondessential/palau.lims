# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bes.lims.interfaces import IBESLimsLayer
from senaite.storage import ISenaiteStorageLayer


class IPalauLimsLayer(IBESLimsLayer,
                      ISenaiteStorageLayer):
    """Zope 3 browser Layer interface specific for palau.lims
    This interface is referred in profiles/default/browserlayer.xml.
    All views and viewlets register against this layer will appear in the site
    only when the add-on installer has been run.
    """
