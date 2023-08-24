# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims.interfaces import IDoNotSupportSnapshots
from senaite.ast import ISenaiteASTLayer
from senaite.core.interfaces import IHideActionsMenu
from senaite.core.interfaces import ISenaiteCore
from senaite.impress.interfaces import ILayer as ISenaiteImpressLayer
from senaite.lims.interfaces import ISenaiteLIMS
from senaite.patient import ISenaitePatientLayer


class IPalauLimsLayer(ISenaiteCore,
                      ISenaiteLIMS,
                      ISenaiteImpressLayer,
                      ISenaiteASTLayer,
                      ISenaitePatientLayer):
    """Zope 3 browser Layer interface specific for palau.lims
    This interface is referred in profiles/default/browserlayer.xml.
    All views and viewlets register against this layer will appear in the site
    only when the add-on installer has been run.
    """
