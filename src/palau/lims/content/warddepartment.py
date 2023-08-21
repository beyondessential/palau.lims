# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd


from plone.dexterity.content import Container
from plone.supermodel import model
from senaite.core.catalog import SETUP_CATALOG
from zope.interface import implementer


class IWardDepartment(model.Schema):
    """Ward Department content interface
    """
    # Implements IBasic behavior (title + description)
    pass


@implementer(IWardDepartment)
class WardDepartment(Container):
    """Ward Department content
    """
    # Catalogs where this type will be catalogued
    _catalogs = [SETUP_CATALOG]
