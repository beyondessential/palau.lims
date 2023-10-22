# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from AccessControl import ClassSecurityInfo
from bika.lims import api
from Products.Archetypes.Registry import registerWidget
from senaite.core.browser.widgets import ReferenceWidget


class ReferenceOtherWidget(ReferenceWidget):
    """A widget that allows the user to choose from several pre-existing
    options along with an 'Other' option. When the latter is selected, user
    can also add free-text in addition to the option(s) already selected.
    """
    security = ClassSecurityInfo()

    base_klass = ReferenceWidget.klass
    klass = "{} {}".format(base_klass, u"palau-referenceother-widget-input")

    _properties = ReferenceWidget._properties.copy()
    _properties.update({
        "macro": "palau_widgets/referenceotherwidget",
    })

    @security.public
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False):

        field_name = field.getName()
        value = form.get(field_name, None)

        if isinstance(value, dict):
            uids = value.get("refs", [])
            other = value.get("other_text", "")
        else:
            uids = value
            check_subfield = "{}_checkbox".format(field_name)
            other_subfield = "{}_other".format(field_name)

            other = ""
            store_other = form.get(check_subfield)
            if self.is_true(store_other):
                other = form.get(other_subfield, "")

        # Resolve the uids
        value = {
            "refs": self.to_uids(uids),
            "other_text": other
        }
        return value, {}

    def to_uids(self, value):
        uids = []
        if api.is_string(value):
            uids = value.split("\r\n")
        if isinstance(value, (list, tuple, set)):
            uids = filter(api.is_uid, value)
        elif api.is_object(value):
            uids = [api.get_uid(value)]
        return uids

    def is_true(self, value):
        """Returns whether val evaluates to True
        """
        value = str(value).strip().lower()
        return value in ["y", "yes", "1", "true", "on"]


# Register widgets
registerWidget(ReferenceOtherWidget, title="ReferenceOtherWidget")
