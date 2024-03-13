# -*- coding: utf-8 -*-

from palau.lims.tamanu.api import get_tamanu_uid
from palau.lims.tamanu.interfaces import ITamanuContent
from plone.indexer import indexer


@indexer(ITamanuContent)
def tamanu_uid(instance):
    """Indexes the UID of this instance at Tamanu
    """
    return get_tamanu_uid(instance)
