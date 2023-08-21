# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from plone.dexterity.content import Container
from palau.lims.interfaces import IClinicalInformations
from zope.interface import implementer


@implementer(IClinicalInformations)
class ClinicalInformations(Container):
    """Folder for clinical informations
    """
    # Catalogs where this type will be catalogued
    _catalogs = ["uid_catalog", "portal_catalog"]
