# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bes.lims.extender.field import ExtensionField
from bika.lims import api
from Products.Archetypes.Field import LinesField


class ExtSiteField(ExtensionField, LinesField):
    """Extended Field for Site
    """

    def get(self, instance, **kw):
        return getattr(instance, "_sample_point", None)

    def set(self, instance, value, **kw):
        if api.is_string(value):
            value = filter(None, value.split("\r\n"))

        if not isinstance(value, (tuple, list, set)):
            value = tuple((value, ))
        out = set()
        # reset sample point
        sample_point = instance.getField("SamplePoint")
        sample_point.set(instance, None)
        for val in value:
            if api.is_uid(val):
                val = api.get_object_by_uid(val, default=None)
            if api.is_object(val):
                obj = api.get_object(val)
                val = api.get_title(obj)
                # proxy to sample point
                uid = api.get_uid(obj)
                sample_point.set(instance, uid)
            if val and api.is_string(val):
                out.add(val)
        setattr(instance, "_sample_point", tuple(out))
