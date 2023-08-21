# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from palau.lims.utils import get_field_value
from palau.lims.utils import set_field_value


def setContainerWidget(self, value):  # noqa CamelCase
    """Setter for the ContainerWidget field
    """
    set_field_value(self, "ContainerWidget", value)


def getContainerWidget(self):  # noqa CamelCase
    """Getter for the ContainerWidget field
    """
    return get_field_value(self, "ContainerWidget")


def setMaximumVolume(self, value):  # noqa CamelCase
    """Setter for the ContainerWidget field
    """
    set_field_value(self, "MaximumVolume", value)


def getMaximumVolume(self):  # noqa CamelCase
    """Setter for the ContainerWidget field
    """
    return get_field_value(self, "MaximumVolume")
