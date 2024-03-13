# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from palau.lims.tamanu.config import TAMANU_STORAGE
from palau.lims.tamanu.interfaces import ITamanuContent
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations

_marker = object


def is_tamanu_content(obj):
    """Returns whether the object passed has a counterpart content at Tamanu
    """
    return ITamanuContent.providedBy(obj)


def get_tamanu_storage(obj):
    """Get or creates the Tamanu storage for the given object

    :param obj: Content object
    :returns: PersistentDict
    """
    annotation = IAnnotations(obj)
    if annotation.get(TAMANU_STORAGE) is None:
        annotation[TAMANU_STORAGE] = PersistentDict()
    return annotation[TAMANU_STORAGE]


def get_tamanu_uid(obj):
    """Returns the UID of the counterpart content at Tamanu, if any
    """
    storage = get_tamanu_storage(obj)
    return storage.get("uid", None)
