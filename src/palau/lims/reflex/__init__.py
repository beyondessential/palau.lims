# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

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
