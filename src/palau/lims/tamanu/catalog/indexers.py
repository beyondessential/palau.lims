# -*- coding: utf-8 -*-

from palau.lims.tamanu.interfaces import ITamanuContent
from plone.indexer import indexer


@indexer(ITamanuContent)
def tamanu_uid(instance):
    """Indexes the UID of this instance at Tamanu
    """
    return getattr(instance, "tamanu_uid", None)
