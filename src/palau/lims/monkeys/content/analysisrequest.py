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


def getClinicalInformation(self):
    """Returns the clinical information objects assigned to the sample
    """
    return self.getField("ClinicalInformation").get(self)


def getRawClinicalInformation(self):
    """Returns the UIDs of the clinical informations assigned to this sample
    """
    return self.getField("ClinicalInformation").getRaw(self)


def getClinicalInformationOtherText(self):
    """Returns the "Other..." text assigned for ClinicalInformation field
    """
    return self.getField("ClinicalInforation").getOtherText(self)


def setClinicalInformationOtherText(self, value):
    """Sets the value for the "Other..." option for ClinicalInformation field
    """
    self.getField("ClinicalInformation").setOtherText(self, value)
