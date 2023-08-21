# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from bika.lims.browser.analysisrequest.view import AnalysisRequestViewView
from palau.lims import utils
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SampleView(AnalysisRequestViewView):
    """Sample view that overrides core's default
    """
    template = ViewPageTemplateFile("templates/sample_view.pt")

    def get_heading(self):
        """Returns the heading to display inside documentFirstHeading
        section of the view
        """
        # Sample info
        sample = self.context
        date_sampled = sample.getDateSampled()
        date_sampled = utils.to_localized_time(date_sampled, long_format=False)

        # Patient info
        patient_name = sample.getPatientFullName() or ""
        patient_mrn = sample.getMedicalRecordNumberValue() or ""

        # Sample template
        sample_template = sample.getTemplate() or ""
        if sample_template:
            sample_template = api.get_title(sample_template)

        values = [
            patient_name,
            patient_mrn,
            date_sampled,
            sample_template
        ]
        values = filter(None, values)
        values = utils.to_utf8(values)
        return " · ".join(values)
