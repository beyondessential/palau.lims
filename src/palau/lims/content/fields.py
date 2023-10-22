# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from archetypes.schemaextender.field import ExtensionField as BaseExtField
from bika.lims.browser.fields import UIDReferenceField
from palau.lims.schema.uidreferenceotherfield import UIDReferenceOtherField
from plone.app.blob.field import ImageField as BlobImageField
from Products.Archetypes.Field import BooleanField
from Products.Archetypes.Field import IntegerField
from Products.Archetypes.Field import StringField
from Products.Archetypes.Field import TextField
from senaite.core.browser.fields.datetime import DateTimeField
from senaite.core.browser.fields.records import RecordsField


class ExtensionField(BaseExtField):
    """Mix-in class to make Archetypes fields not depend on generated
    accessors and mutators, and use AnnotationStorage by default
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


class ExtUIDReferenceOtherField(ExtensionField, UIDReferenceOtherField):
    """Field extender of png.lims.schema.UIDReferenceOtherField
    """
