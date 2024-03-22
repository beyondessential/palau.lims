# -*- coding: utf-8 -*-

from palau.lims.tamanu.api import get_tamanu_uid


def tamanu_uid(self):
    """Returns the tamanu UID of the given object, if any
    """
    return get_tamanu_uid(self)
