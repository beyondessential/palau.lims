# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from palau.lims.tamanu.config import TAMANU_STORAGE
from palau.lims.tamanu.interfaces import ITamanuContent
from palau.lims.tamanu.interfaces import ITamanuResource
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations

_marker = object


def is_tamanu_content(obj):
    """Returns whether the object passed has a counterpart content at Tamanu
    """
    return ITamanuContent.providedBy(obj)


def is_tamanu_resource(obj):
    """Returnsw whether the object passed in is a Tamanu's HL7 resource
    """
    return ITamanuResource.providedBy(obj)


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
    if is_tamanu_resource(obj):
        return obj.UID()

    storage = get_tamanu_storage(obj)
    return storage.get("uid", None)


def get_brain_by_tamanu_uid(uid, default=None):
    """Query a brain by a given Tamanu UID
    """
    if not uid:
        return default

    uc = api.get_tool(api.UID_CATALOG)
    brains = uc(UID=uid)
    if len(brains) != 1:
        return default
    return brains[0]


def get_object_by_tamanu_uid(uid, default=_marker):
    """Returns the object for the given Tamanu UID

    :param uid: The Tamanu UID to search by
    :type uid: string
    :returns: Found Object or default
    """
    if not uid:
        if default is not _marker:
            return default
        raise ValueError("uid not set")

    brain = get_brain_by_tamanu_uid(uid)
    if not brain:
        if default is not _marker:
            return default
        raise ValueError("No object found for tamanu_uid {}".format(uid))

    return api.get_object(brain)


def get_object(thing, default=_marker):
    """Get the full content object
    """
    if is_tamanu_resource(thing):
        return get_object_by_tamanu_uid(thing.UID(), default=default)

    # rely on core's api
    if default is _marker:
        return api.get_object(thing)

    return api.get_object(thing, default=default)
