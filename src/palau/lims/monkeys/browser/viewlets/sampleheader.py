# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from palau.lims.content.fields import ExtUIDReferenceOtherField
from senaite.core.browser.viewlets.sampleheader import _fieldname_not_in_form


def get_field_value(self, field, form):
    """Returns the submitted value for the given field
    """
    fieldname = field.getName()
    if fieldname not in form:
        return _fieldname_not_in_form

    value = form[fieldname]

    # Handle custom UIDReferenceOtherFields
    if isinstance(field, ExtUIDReferenceOtherField):
        other_fieldname = "{}_other".format(fieldname)
        value = {
            "refs": value,
            "other_text": form.get(other_fieldname, u'')
        }

    return value
