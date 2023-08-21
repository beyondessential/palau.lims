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

    fieldvalue = form[fieldname]

    # Handle (multiValued) reference fields
    # https://github.com/bikalims/bika.lims/issues/2270
    uid_fieldname = "{}_uid".format(fieldname)
    if uid_fieldname in form:
        # get the value from the corresponding `uid_<fieldname>` key
        value = form[uid_fieldname]

        # extract the assigned UIDs for multi-reference fields
        if field.multiValued:
            value = filter(None, value.split(","))

        # allow to flush single reference fields
        if not field.multiValued and not fieldvalue:
            value = ""

        # Handle custom UIDReferenceOtherFields
        if isinstance(field, ExtUIDReferenceOtherField):
            other_fieldname = "{}_other".format(fieldname)
            value = {
                "refs": value,
                "other_text": form.get(other_fieldname, u'')
            }

        return value

    # other fields
    return fieldvalue
