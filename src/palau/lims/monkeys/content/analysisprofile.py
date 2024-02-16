# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from palau.lims.behaviors.analysisprofile import IPalauAnalysisProfileBehavior


def getSampleTypes(self):
    """Returns the sample types assigned to this object, if any
    """
    behavior = IPalauAnalysisProfileBehavior(self)
    return behavior.getSampleTypes()


def getRawSampleTypes(self):
    """Returns the UIDs of the sample types assigned to this object if any
    """
    behavior = IPalauAnalysisProfileBehavior(self)
    return behavior.getRawSampleTypes()


def setSampleTypes(self, value):
    """Sets the sample types assigned to this object, if any
    """
    behavior = IPalauAnalysisProfileBehavior(self)
    return behavior.setSampleTypes(value)
