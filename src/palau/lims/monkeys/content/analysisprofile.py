# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd


def getSampleTypes(self):
    """Returns the sample types assigned to this object, if any
    """
    return self.getField("SampleTypes").get(self)


def getRawSampleTypes(self):
    """Returns the UIDs of the sample types assigned to this object if any
    """
    return self.getField("SampleTypes").getRaw(self)


def setSampleTypes(self, value):
    """Sets the sample types assigned to this object, if any
    """
    return self.getField("SampleTypes").set(self, value)
