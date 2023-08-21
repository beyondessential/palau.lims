# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from plone.dexterity.content import Item
from palau.lims.interfaces import IClinicalInformation
from Products.Archetypes.config import UID_CATALOG
from senaite.core.catalog import SETUP_CATALOG
from zope.interface import implementer


@implementer(IClinicalInformation)
class ClinicalInformation(Item):
    """ArchiveItem content
    """
    # Catalogs where this type will be catalogued
    _catalogs = [UID_CATALOG, SETUP_CATALOG]
