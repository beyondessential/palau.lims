# -*- coding: utf-8 -*-

from palau.lims.tamanu import logger
from palau.lims.tamanu.interfaces import ITamanuResource
from zope.interface import implementer


_marker = object()


@implementer(ITamanuResource)
class TamanuResource(object):

    _refs = {}

    def __init__(self, session, data=None):
        self._session = session
        self._data = data or {}

    def wrap(self, data):
        self._data = data
        return self

    def UID(self):
        """Returns the Tamanu UID of this resource
        """
        return self.get_raw("id")

    def get_raw(self, field_name, default=None):
        return self._data.get(field_name, default)

    def is_reference(self, record):
        if not isinstance(record, dict):
            return False
        reference_id = record.get("reference")
        if reference_id:
            return True
        return False

    def get_reference(self, record_or_id):
        if isinstance(record_or_id, dict):
            ref_id = record_or_id.get("reference")
        else:
            ref_id = record_or_id
        reference = self._refs.get(ref_id)
        if not reference:
            item = self._session.get(ref_id)
            reference = self._session.to_resource(item)
            if not reference:
                logger.error("Cannot resolve reference for {}"
                             .format(repr(record_or_id)))
                return None
            self._refs[ref_id] = reference
        return self._refs[ref_id]

    def get(self, field_name, default=None):
        record = self.get_raw(field_name, _marker)
        if record is _marker:
            return default

        # is this record a reference
        if self.is_reference(record):
            return self.get_reference(record)

        return record

    def __repr__(self):
        return repr(self._data)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()
