# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerWidget
from senaite.core.browser.widgets import ReferenceWidget
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


class ReferenceOtherWidget(ReferenceWidget):
    """A widget that allows the user to choose from several pre-existing options
    along with an 'Other' option. When the latter is selected, user can also
    add free-text in addition to the option(s) already selected.
    """
    security = ClassSecurityInfo()
    _properties = ReferenceWidget._properties.copy()
    _properties.update({
       "macro": "palau_widgets/referenceotherwidget",
    })

    @security.public
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False):

        out = super(ReferenceOtherWidget, self).process_form(
            instance, field, form, empty_marker=empty_marker,
            emptyReturnsMarker=emptyReturnsMarker)

        # Extract the value entered for Other field
        other_id = "{}_other".format(field.getName())
        other_value = form.get(other_id, u'')

        # Set the value for field's Other attr
        field.setOtherText(instance, other_value)

        return out


# Register widgets
registerWidget(BottlesWidget, title="BottlesWidget")
registerWidget(ReferenceOtherWidget, title="ReferenceOtherWidget")
