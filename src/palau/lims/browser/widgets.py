# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerWidget
from senaite.core.browser.widgets.recordswidget import RecordsWidget


class BottlesWidget(RecordsWidget):
    """A widget for the selection of BACTEC bottles at once, together with
    their unique identifier (Bottle ID) and weight field
    """
    security = ClassSecurityInfo()
    _properties = RecordsWidget._properties.copy()
    _properties.update({
        "macro": "palau_widgets/bottleswidget",
        "helper_js": ("senaite_widgets/recordswidget.js",),
    })

# Register widgets
registerWidget(BottlesWidget, title="BottlesWidget")
