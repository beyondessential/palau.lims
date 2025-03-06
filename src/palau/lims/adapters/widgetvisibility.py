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

from bika.lims import api
from bika.lims.adapters.widgetvisibility import SenaiteATWidgetVisibility


class ContainerFieldVisibility(SenaiteATWidgetVisibility):
    """Handles Container field visibility in Sample add form and view
    """

    def __init__(self, context):
        super(ContainerFieldVisibility, self).__init__(
            context=context, sort=10, field_names=["Container"])

    def isVisible(self, field, mode="view", default="visible"):
        if mode in ["edit", "view"]:
            # Render the Container only if the Sample Type from the Sample does
            # specify that the container widget must be used
            sample_type = self.context.getSampleType()
            widget = sample_type.getContainerWidget()
            if widget != "container":
                return "invisible"

        return default


class BottlesFieldVisibility(SenaiteATWidgetVisibility):
    """Handles Bottles field visibility in Sample add form and view
    """

    def __init__(self, context):
        super(BottlesFieldVisibility, self).__init__(
            context=context, sort=10, field_names=["Bottles"])

    def isVisible(self, field, mode="view", default="visible"):
        if mode in ["edit", "view"]:
            # Render the Container only if the Sample Type from the Sample does
            # specify that the container widget must be used
            sample_type = self.context.getSampleType()
            widget = sample_type.getContainerWidget()
            if widget != "bottles":
                return "invisible"

        return default


class PrimaryAnalysisRequestFieldVisibility(SenaiteATWidgetVisibility):
    """Handles the visibility in Sample add form and view
    """

    def __init__(self, context):
        super(PrimaryAnalysisRequestFieldVisibility, self).__init__(
            context=context, sort=10, field_names=["PrimaryAnalysisRequest"])

    def isVisible(self, field, mode="view", default="visible"):
        if mode == "add":
            # Do not display the field unless primaries in the url
            request = api.get_request()
            primaries = request.get("primary", "")
            primaries = filter(api.is_uid, primaries.split(","))
            if primaries:
                return "edit"
            return "invisible"

        return default
