# -*- coding: utf-8 -*-
from palau.lims.behaviors.sampletemplate import IExtendedSampleTemplateBehavior


def get_behavior(context):
    return IExtendedSampleTemplateBehavior(context)


def getMinimumVolume(self):
    behavior = get_behavior(self)
    return behavior.getMinimumVolume()


def setMinimumVolume(self, value):
    behavior = get_behavior(self)
    behavior.setMinimumVolume(value)


def getInsufficientVolumeText(self):
    behavior = get_behavior(self)
    return behavior.getInsufficientVolumeText()


def setInsufficientVolumeText(self, value):
    behavior = get_behavior(self)
    behavior.setInsufficientVolumeText(value)
