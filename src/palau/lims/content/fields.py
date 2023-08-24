# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import six
from archetypes.schemaextender.interfaces import IExtensionField
from bika.lims.browser.fields import UIDReferenceField
from plone.app.blob.field import ImageField as BlobImageField
from Products.Archetypes.Field import BooleanField
from Products.Archetypes.Field import IntegerField
from Products.Archetypes.Field import StringField
from Products.Archetypes.Field import TextField
from Products.Archetypes.Storage.annotation import AnnotationStorage
from senaite.core.browser.fields.records import RecordsField
from zope.interface import implementer
from zope.component.hooks import getSite
from senaite.core.browser.fields.datetime import DateTimeField


@implementer(IExtensionField)
class ExtensionField(object):
    """Mix-in class to make Archetypes fields not depend on generated
    accessors and mutators, and use AnnotationStorage by default
    """

    storage = AnnotationStorage()

    def __init__(self, *args, **kwargs):
        super(ExtensionField, self).__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

    def getAccessor(self, instance):
        """Return the accessor method for getting data out of this field
        """
        def accessor():
            if self.getType().endswith('ReferenceField'):
                return self.get(instance.__of__(getSite()))
            else:
                return self.get(instance)
        return accessor

    def getEditAccessor(self, instance):
        """Return the accessor method for getting raw data out of this field
        e.g.: for editing.
        """
        def edit_accessor():
            if self.getType().endswith('ReferenceField'):
                return self.getRaw(instance.__of__(getSite()))
            else:
                return self.getRaw(instance)
        return edit_accessor

    def getMutator(self, instance):
        """Return the mutator method used for changing the value of this field.
        """
        def mutator(value, **kw):
            if self.getType().endswith('ReferenceField'):
                self.set(instance.__of__(getSite()), value)
            else:
                self.set(instance, value)
        return mutator

    def getIndexAccessor(self, instance):
        """Return the index accessor, i.e. the getter for an indexable value.
        """
        name = getattr(self, 'index_method', None)
        if name is None or name == '_at_accessor':
            return self.getAccessor(instance)
        elif name == '_at_edit_accessor':
            return self.getEditAccessor(instance)
        elif not isinstance(name, six.string_types):
            raise ValueError('Bad index accessor value: %r', name)
        else:
            return getattr(instance, name)


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
