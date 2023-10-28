# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

def getRawWard(self):
    """Returns the UID of the Ward assigned to the sample, if any
    """
    return self.getField("Ward").getRaw(self)


def getWard(self):
    """Returns the Ward object assigned to the sample, if any
    """
    return self.getField("Ward").get(self)


def setWard(self, value):
    """Assigns the ward to the sample
    """
    self.getField("Ward").set(self, value)


def getSite(self):
    """Returns the Site assigned to the sample, if any
    """
    return self.getField("Site").get(self)


def setSite(self, value):
    """Assigns the site to the sample
    """
    self.getField("Site").set(self, value)


def getClinicalInformation(self):
    """Returns the clinical information from the sample
    """
    return self.getField("ClinicalInformation").get(self)


def setClinicalInformation(self, value):
    """Assigns the clinical information to the sample
    """
    self.getField("ClinicalInformation").set(self, value)
