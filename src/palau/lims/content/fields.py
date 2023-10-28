# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from archetypes.schemaextender.field import ExtensionField as ATExtensionField
from bika.lims import api
from bika.lims.browser.fields import UIDReferenceField
from plone.app.blob.field import ImageField as BlobImageField
from Products.Archetypes.Field import BooleanField
from Products.Archetypes.Field import IntegerField
from Products.Archetypes.Field import LinesField
from Products.Archetypes.Field import StringField
from Products.Archetypes.public import TextField
from senaite.core.browser.fields.datetime import DateTimeField
from senaite.core.browser.fields.records import RecordsField


class ExtensionField(ATExtensionField):
    """Mix-in class to make Archetypes fields not depend on generated accessors
    and mutators, and use AnnotationStorage by default
    """

    def __init__(self, *args, **kwargs):
        super(ExtensionField, self).__init__(*args, **kwargs)


class ExtBooleanField(ExtensionField, BooleanField):
    """Field extender of BooleanField
    """


class ExtIntegerField(ExtensionField, IntegerField):
    """Field extender of IntegerField
    """


class ExtStringField(ExtensionField, StringField):
    """Field extender of StringField
    """


class ExtTextField(ExtensionField, TextField):
    """Field extender of TextField
    """


class ExtUIDReferenceField(ExtensionField, UIDReferenceField):
    """Field Extender of core's UIDReferenceField for AT types
    """


class ExtRecordsField(ExtensionField, RecordsField):
    """Field Extender of RecordsField
    """


class ExtBlobImageField(ExtensionField, BlobImageField):
    """Field extender of plone.app.blob's ImageField
    """


class ExtDateTimeField(ExtensionField, DateTimeField):
    """Field extender of senaite.core.browser.fields.DateTimeField
    """


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
