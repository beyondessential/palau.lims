# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims.browser.fields import UIDReferenceField
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations
from AccessControl import ClassSecurityInfo


OTHER_TEXT_STORAGE = "palau.lims.schema.uidreferenceotherfield.other"


def get_other_text_storage(context):
    """Returns the annotation storage for the other text property
    """
    annotation = IAnnotations(context)
    if annotation.get(OTHER_TEXT_STORAGE) is None:
        annotation[OTHER_TEXT_STORAGE] = PersistentDict()
    return annotation[OTHER_TEXT_STORAGE]


class UIDReferenceOtherField(UIDReferenceField):
    """Fields that besides keeping references to existing UIDs, it can also
    store a text-free value (usually for 'Other' options)

    Note this is for AT-like objects only!
    """
    security = ClassSecurityInfo()

    @security.public
    def set(self, context, value, **kwargs):
        if isinstance(value, dict):

            # Store the other text
            other = value.get("other_text", "")
            self.setOtherText(context, other)

            # Set the uids
            value = value.get("refs", "")

        super(UIDReferenceOtherField, self).set(context, value, **kwargs)

    @security.public
    def getOtherText(self, obj):  # noqa CamelCase
        """Returns the 'Other comment' assigned for this object and field
        """
        storage = get_other_text_storage(obj)
        return storage.get("text", u'')

    @security.public
    def setOtherText(self, obj, value):  # noqa CamelCase
        """Stores the text value for the 'Other comment' field
        """
        storage = get_other_text_storage(obj)
        storage["text"] = value
