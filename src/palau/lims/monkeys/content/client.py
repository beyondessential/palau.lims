# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd


def getWardDepartmentRequired(self):
    """Returns whether the input for WardDepartment field for samples belonging
    to this client is required
    """
    return self.getField("WardDepartmentRequired").get(self)


def setWardDepartmentRequired(self, value):
    """Sets whether the input for WardDepartment field for samples belonging
    to this client is required
    """
    self.getField("WardDepartmentRequired").set(self, value)
