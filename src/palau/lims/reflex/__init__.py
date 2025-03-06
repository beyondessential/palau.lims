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

from zope.component import queryAdapter
from zope.interface import implements
from zope.interface import Interface


class IReflexTesting(Interface):
    """Marker interface for Reflex Testing Adapters
    """

    def __call__(self):
        """Executes the reflex testing for the analysis
        """


class ReflexTestingBaseAdapter(object):
    """Base Reflex Testing Adapter
    """
    implements(IReflexTesting)

    def __init__(self, analysis):
        self.analysis = analysis


def handle_reflex_testing(analysis, action):
    """Handles the reflex testing for the given analysis and action, if any
    """
    keyword = analysis.getKeyword()

    # Replace special characters from the keyword
    keyword = keyword.replace("-", "")
    keyword = keyword.lower()

    # Run CINTER's reflex testing when keyword *starts* with CINTER
    # https://github.com/beyondessential/pnghealth.lims/issues/127
    if keyword.startswith("cinter"):
        keyword = "cinter"

    name = "palau.lims.reflex.{}.{}".format(keyword, action)
    adapter = queryAdapter(analysis, IReflexTesting, name=name)
    if adapter:
        adapter()
