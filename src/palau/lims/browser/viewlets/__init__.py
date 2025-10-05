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

from plone.app.layout.viewlets import ViewletBase
from palau.lims import utils
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from senaite.core.api import measure as mapi


# TODO Port UnknownDoctorViewlet to bes.lims
class UnknownDoctorViewlet(ViewletBase):
    """Print a viewlet to display a message string that the Doctor assigned to
    the current Sample is Unknown
    """
    index = ViewPageTemplateFile("templates/unknown_doctor_viewlet.pt")

    def __init__(self, context, request, view, manager=None):
        super(UnknownDoctorViewlet, self).__init__(
            context, request, view, manager=manager)
        self.context = context
        self.request = request
        self.view = view

    def is_visible(self):
        """Returns whether this viewlet must be visible or not
        """
        contact = self.context.getContact()
        return utils.is_unknown_doctor(contact)


# TODO Port NotEnoughSampleViewlet to bes.lims
class NotEnoughSampleViewlet(ViewletBase):
    """Print a viewlet to display a message string that the Volume assigned to
    the sample is not enough based on the minimum volume set in the assigned
    template or Sample Type
    """
    index = ViewPageTemplateFile("templates/not_enough_sample_viewlet.pt")

    def __init__(self, context, request, view, manager=None):
        super(NotEnoughSampleViewlet, self).__init__(
            context, request, view, manager=manager)
        self.context = context
        self.request = request
        self.view = view

    def get_minimum_volume(self):
        """Returns the minimum volume
        """
        return utils.get_minimum_volume(self.context)

    def is_visible(self):
        """Returns whether this viewlet must be visible or not
        """
        return not utils.is_enough_volume(self.context)


# TODO Port OverSampleViewlet to bes.lims
class OverSampleViewlet(ViewletBase):
    """Print a viewlet to display a message string that the Volume assigned to
    the sample is over based on the maximum volume set in the assigned
    template or Sample Type
    """
    index = ViewPageTemplateFile("templates/over_sample_viewlet.pt")

    def __init__(self, context, request, view, manager=None):
        super(OverSampleViewlet, self).__init__(
            context, request, view, manager=manager)
        self.context = context
        self.request = request
        self.view = view

    def get_maximum_volume(self):
        """Returns the maximum volume
        """
        return utils.get_maximum_volume(self.context)

    def is_visible(self):
        """Returns whether this viewlet must be visible or not
        """
        # Get the expected minimum volume
        obj = self.context
        max_volume = self.get_maximum_volume()
        if not max_volume or not mapi.is_volume(max_volume):
            return False

        # Get the sample's volume
        obj_volume = obj.getField("Volume").get(obj)

        # Convert them to magnitude and compare
        max_volume = mapi.get_magnitude(max_volume)
        obj_volume = mapi.get_magnitude(obj_volume, default="0 ml")
        return obj_volume > max_volume


# TODO Port ErrorDateOfAdmissionViewlet to bes.lims
class ErrorDateOfAdmissionViewlet(ViewletBase):
    """Print a viewlet to display an error message if the Date of Admission
    (date and time) is after the Sampled Date (date and time).
    (An error occurs when Date of Admission is after Sampled Date.
    It is accepted when Date of Admission is before or equal Sampled Date.)
    """
    index = ViewPageTemplateFile(
        "templates/error_date_of_admission_viewlet.pt"
    )

    def __init__(self, context, request, view, manager=None):
        super(ErrorDateOfAdmissionViewlet, self).__init__(
            context, request, view, manager=manager)
        self.context = context
        self.request = request
        self.view = view

    def get_date_sampled(self):
        """Return the sampled date
        """
        obj = self.context
        return obj.getDateSampled()

    def localize(self, date, **kwargs):
        """Converts the given date to a localized time string
        """
        return utils.to_localized_time(date, **kwargs)

    def is_visible(self):
        """Returns whether this viewlet must be visible or not
        """
        # Get the date sampled
        obj = self.context
        date_sampled = self.get_date_sampled()

        if not date_sampled:
            return False

        # Get the date of admission
        date_of_admission = obj.getField("DateOfAdmission").get(obj)
        return date_of_admission > date_sampled
