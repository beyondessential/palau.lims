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
from palau.lims import messageFactory as _
from senaite.core.api import measure as mapi
from senaite.core.browser.form.adapters import EditFormAdapterBase

FIELDS = {
    "SampleTemplate": {
        "SampleType": "form.widgets.sampletype",
        "MinimumVolume":
            "form.widgets.IExtendedSampleTemplateBehavior.minimum_volume",
    }
}


class SampleTemplateEditForm(EditFormAdapterBase):
    """Edit form adapter for Sample Template
    """

    def get_field_id(self, field_name):
        fields = FIELDS.get("SampleTemplate", {})
        return fields.get(field_name, field_name)

    def initialized(self, data):
        # Validate the Minimum Volume field
        self.validate_minimum_volume(data)
        return self.data

    def modified(self, data):
        name = data.get("name")
        fields = ["MinimumVolume", "SampleType"]
        fields_ids = [self.get_field_id(field) for field in fields]
        if name in fields_ids:
            # Validate the Minimum Volume field
            self.validate_minimum_volume(data)

        return self.data

    def get_minimum_volume(self, data):
        """Returns the Minimum Volume set for this AR Template, if set. Returns
        None otherwise
        """
        form = data.get("form")
        field_id = self.get_field_id("MinimumVolume")
        return form.get(field_id) or None

    def get_sample_type_minimum_volume(self, data):
        """Returns the minimum volume of the Sample Type currently selected, if
        any. Otherwise, returns None
        """
        form = data.get("form")
        field_id = self.get_field_id("SampleType")
        sample_type_uid = form.get(field_id)
        if not api.is_uid(sample_type_uid):
            return None
        sample_type = api.get_object_by_uid(sample_type_uid)
        return sample_type.getMinimumVolume()

    def validate_minimum_volume(self, data):
        """Validates the Minimum Volume set in the AR Template form is below
        the Minimum Volume set to the assigned Sample Type
        """
        error_msg = ""

        # Get the volume of the Sample Type assigned to the Sample Template
        st_min_volume = self.get_sample_type_minimum_volume(data)
        if st_min_volume:
            # Minimum Volume assigned to the Sample Template
            min_volume = self.get_minimum_volume(data)

            # Convert to magnitude for proper comparison
            st_mg_volume = mapi.get_magnitude(st_min_volume, default="0ml")
            mg_volume = mapi.get_magnitude(min_volume, default="0ml")

            # Compare
            if mg_volume < st_mg_volume:
                error_msg = _("Volume is below {}").format(st_min_volume)

        # Set or clear the field error message
        field_id = self.get_field_id("MinimumVolume")
        self.add_error_field(field_id, error_msg)


class ContainerEditForm(EditFormAdapterBase):
    """Edit form adapter for Container
    """

    def initialized(self, data):
        return self.data

    def modified(self, data):
        name = data.get("name")
        value = data.get("value")
        if name == "form.widgets.IExtendedSampleContainerBehavior.weight":
            self.add_error_field(name, self.validate_weight(value))

        return self.data

    def validate_weight(self, value):
        """Checks the value is a valid weight
        """
        message = ""
        if value and not mapi.is_weight(value):
            message = _("Not a valid quantity or unit")

        return message
