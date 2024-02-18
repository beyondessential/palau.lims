# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from palau.lims.behaviors.analysisprofile import IPalauAnalysisProfileBehavior


def get_behavior(obj):
    """Returns the IPalauAnalysisProfileBehavior for the given obj if set
    """
    try:
        return IPalauAnalysisProfileBehavior(obj)
    except TypeError:
        return None


def getSampleTypes(self):
    """Returns the sample types assigned to this object, if any
    """
    behavior = get_behavior(self)
    if not behavior:
        return []
    return behavior.getSampleTypes()


def getRawSampleTypes(self):
    """Returns the UIDs of the sample types assigned to this object if any
    """
    behavior = get_behavior(self)
    if not behavior:
        return []
    return behavior.getRawSampleTypes()


def setSampleTypes(self, value):
    """Sets the sample types assigned to this object, if any
    """
    behavior = get_behavior(self)
    if behavior:
        behavior.setSampleTypes(value)
