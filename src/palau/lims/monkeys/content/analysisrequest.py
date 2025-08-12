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


def getRawWardDepartment(self):
    """Returns the UID of the WardDepartment object assigned to the sample
    """
    return self.getField("WardDepartment").getRaw(self)


def getWardDepartment(self):
    """Returns the WardDepartment object assigned to the sample, if any
    """
    return self.getField("WardDepartment").get(self)


def setWardDepartment(self, value):
    """Returns the WardDepartment object assigned to the sample, if any
    """
    self.getField("WardDepartment").set(self, value)


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


def setResultsInterpretationDepts(self, value):
    """Custom setter which converts inline images to attachments

    https://github.com/senaite/senaite.core/pull/1344

    :param value: list of dictionary records
    """
    if not isinstance(value, list):
        raise TypeError("Expected list, got {}".format(type(value)))

    # Inject the current user
    current_user = api.get_current_user().id

    # Get the original values and group by uid to make comparison easier
    original = self.getField("ResultsInterpretationDepts").get(self)
    original = dict(map(lambda item: (item.get("uid"), item), original))

    # Convert inline images -> attachment files
    records = []
    for record in value:
        # N.B. we might here a ZPublisher record. Converting to dict
        #      ensures we can set values as well.
        record = dict(record)
        # Handle inline images in the HTML
        html = record.get("richtext", "")
        # Process inline images to attachments
        richtext = self.process_inline_images(html)
        record["richtext"] = richtext

        # Compare with original value and if different, overwrite user
        record_uid = record.get("uid")
        original_record = original.get(record_uid) or {}
        if richtext != original_record.get("richtext"):
            user = current_user
        else:
            user = original_record.get("user") or current_user

        # assign the user who submitted the interpretation
        record["user"] = user

        # append the processed record for storage
        records.append(record)

        # set the field
        self.getField("ResultsInterpretationDepts").set(self, records)
