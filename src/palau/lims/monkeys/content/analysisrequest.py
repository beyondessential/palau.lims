# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd
from bika.lims import logger

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


def setResultsInterpretationDepts(self, value):
    """Custom setter which converts inline images to attachments

    https://github.com/senaite/senaite.core/pull/1344

    :param value: list of dictionary records
    """
    value, user = value
    if not isinstance(value, list):
        raise TypeError("Expected list, got {}".format(type(value)))

    # Convert inline images -> attachment files
    records = []
    for record in value:
        # N.B. we might here a ZPublisher record. Converting to dict
        #      ensures we can set values as well.
        record = dict(record)
        # Handle inline images in the HTML
        html = record.get("richtext", "")
        # Process inline images to attachments
        record["richtext"] = self.process_inline_images(html)

        # Add the user associated with this record
        record["user"] = user

        # append the processed record for storage
        records.append(record)

        # set the field
        self.getField("ResultsInterpretationDepts").set(self, records)


def getResultsInterpretationByDepartment(self, department=None):
    """Returns the results interpretation for this Analysis Request
       and department. If department not set, returns the results
       interpretation tagged as 'General'.

    :returns: a dict with the following keys:
        {'uid': <department_uid> or 'general', 'richtext': <text/plain>}
    """
    uid = department.UID() if department else 'general'
    rows = self.Schema()['ResultsInterpretationDepts'].get(self)
    row = [row for row in rows if row.get('uid') == uid]
    if len(row) > 0:
        row = row[0]
        logger.info("Does user subfield exists in this field : {}".format(row.get('user', False)))
    elif uid == 'general' \
            and hasattr(self, 'getResultsInterpretation') \
            and self.getResultsInterpretation():
        row = {'uid': uid, 'richtext': self.getResultsInterpretation()}
    else:
        row = {'uid': uid, 'richtext': ''}
    return row
