# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from palau.lims.tamanu import logger
from palau.lims.tamanu.config import TAMANU_STORAGE
from palau.lims.tamanu.interfaces import ITamanuContent
from palau.lims.tamanu.interfaces import ITamanuResource
from persistent.dict import PersistentDict
from Products.Archetypes.utils import getRelURL
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides

_marker = object

UID_CATALOG = "uid_catalog"


def is_tamanu_content(obj):
    """Returns whether the object passed has a counterpart content at Tamanu
    """
    return ITamanuContent.providedBy(obj)


def is_tamanu_resource(obj):
    """Returns whether the object passed in is a Tamanu's HL7 resource
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
        return obj.UID
    if is_tamanu_content(obj):
        storage = get_tamanu_storage(obj)
        return storage.get("uid", None)
    return None


def get_brain_by_tamanu_uid(uid, default=None):
    """Query a brain by a given Tamanu UID
    """
    if not uid:
        return default

    uc = api.get_tool(api.UID_CATALOG)
    brains = uc(tamanu_uid=uid)
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
        return get_object_by_tamanu_uid(thing.UID, default=default)

    # rely on core's api
    if default is _marker:
        return api.get_object(thing)

    return api.get_object(thing, default=default)


def get_status(thing):
    """Gets the state of a resource or the review state of a SENAITE object
    """
    if is_tamanu_resource(thing):
        return thing.get_raw("status")
    return api.get_review_status(thing)


def create_object(container, resource, **kwargs):
    """Creates an object for the given Tamanu resource
    """
    if not is_tamanu_resource(resource):
        raise ValueError("Type not supported: {}".format(repr(type(resource))))

    # check if the object exists already!
    tamanu_uid = resource.UID
    brain = get_brain_by_tamanu_uid(tamanu_uid)
    if brain:
        raise ValueError("An object with Tamanu's UID {} exists already"
                         .format(tamanu_uid))

    # get the data from the resource
    info = resource.to_object_info()
    info.update(kwargs)

    # get the container and portal_type
    container = api.get_object(container)
    portal_type = info.pop("portal_type")

    # create the object
    obj = api.create(container, portal_type, **info)
    logger.info("Object created: %s" % repr(obj))

    # mark the object with ITamanuContent, so we can always know before hand
    # if this object has a counterpart resource at Tamanu
    alsoProvides(obj, ITamanuContent)

    # assign the tamanu uid, along with current data so we can always use
    # the original information, even when connection with Tamanu is lost
    annotation = get_tamanu_storage(obj)
    annotation["uid"] = tamanu_uid
    annotation["data"] = resource.to_dict()

    # index tamanu_uid from uid_catalog
    catalog_object(obj)

    return obj


def catalog_object(obj):
    """Catalog the object in all registered catalogs
    """
    uid_catalog = api.get_tool(UID_CATALOG)
    if api.is_at_content(obj):
        # For ATs, the uids of uid_catalog are relative paths to portal root
        # see Products.Archetypes.UIDCatalog.UIDResolver.catalog_object
        url = getRelURL(uid_catalog, obj.getPhysicalPath())
    else:
        # For DXs, the uids of uid_catalog are absolute paths to portal root
        # see plone.app.referencablebehavior.uidcatalog
        url = "/".join(obj.getPhysicalPath())

    # explicitly catalog in uid_catalog
    uid_catalog.catalog_object(obj, url)

    # reindex in registered catalogs
    obj.reindexObject()
