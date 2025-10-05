# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS.
#
# PALAU.LIMS is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2023-2025 by it's authors.
# Some rights reserved, see README and LICENSE.

from plone.dexterity.content import Container
from plone.supermodel import model
from senaite.core.catalog import SETUP_CATALOG
from zope.interface import implementer


# TODO Port IWard to bes.lims
class IWard(model.Schema):
    """Ward content interface
    """
    # Implements IBasic behavior (title + description)
    pass


# TODO Port Ward to bes.lims
@implementer(IWard)
class Ward(Container):
    """Ward content
    """
    # Catalogs where this type will be catalogued
    _catalogs = [SETUP_CATALOG]
