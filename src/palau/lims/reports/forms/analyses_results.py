# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from bika.lims import api

from datetime import datetime
from palau.lims import messageFactory as _
from palau.lims.reports import get_analyses
from palau.lims.reports.forms import CSVReport
from palau.lims.utils import get_field_value
from palau.lims.utils import is_reportable
from senaite.core.api import dtime
from senaite.core.catalog import SAMPLE_CATALOG
from senaite.patient.config import SEXES


class AnalysesResults(CSVReport):
    """Analyses by result, category and department
    """

    def process_form(self):
        statuses = ["published"]
        # Collect the analyses filters (date received)
        date_from, date_to = self.parse_date_for_query()

        # Get the filtered analyses list
        brains = get_analyses(date_from, date_to, review_state=statuses)
        objs = map(api.get_object, brains)
        analyses = [analysis for analysis in objs if is_reportable(analysis)]

        # Add the first row (header)
        rows = [[
            _("Sample ID"),
            _("Patient Name"),
            _("Patient Surname"),
            _("Patient Other Names"),
            _("Patient Hospital #"),
            _("Patient Date of Birth"),
            _("Patient Gender"),
            _("Test Date Collected"),
            _("Test Date Tested"),
            _("Test Category"),
            _("Test Department"),
            _("Test ID"),
            _("Test Type"),
            _("Test Result"),
            _("Site"),
            _("Requesting Physician"),
        ]]

        # Add the info per analysis in a row
        for analysis in analyses:
            sample = analysis.getRequest()
            patient_name = get_field_value(
                sample, "PatientFullName", default={}
            )
            dob = self.parse_date_to_output(sample.getDateOfBirth()[0])
            sampled = self.parse_date_to_output(sample.getDateSampled())
            result_captured = self.parse_date_to_output(
                analysis.getResultCaptureDate()
            )

            # Only show results that appear on the final reports
            resultText = ""
            if analysis.getDatePublished():
                resultText = analysis.getFormattedResult() or resultText

            department = analysis.getDepartmentTitle() or ""
            category = analysis.getCategoryTitle() or ""

            # add the info for each analysis in a row
            rows.append(
                [
                    analysis.getRequestID(),
                    patient_name.get("firstname", ""),
                    patient_name.get("lastname", ""),
                    patient_name.get("middlename", ""),
                    sample.getMedicalRecordNumberValue() or "",
                    dob,
                    dict(SEXES).get(sample.getSex(), ""),
                    sampled,
                    result_captured,
                    category,
                    department,
                    analysis.getKeyword(),
                    analysis.Title(),
                    resultText,
                    sample.getClientTitle() or "",
                    sample.getContactFullName() or "",
                ]
            )

        return rows

    def parse_date_for_query(self):
        # Get earliest possible date (first sample date)
        date0 = self.get_first_sample_date()

        # Get latest possible date (today)
        current_date = datetime.now()

        # Set date range
        date_from = self.request.form.get('date_from') or date0
        date_to = self.request.form.get('date_to') or current_date

        # Parse dates for query
        date_from = dtime.to_DT(date_from).earliestTime()
        date_to = dtime.to_DT(date_to).latestTime()

        return date_from, date_to

    def get_first_sample_date(self):
        query = {
            "portal_type": "AnalysisRequest",
            "sort_on": "created",
            "sort_order": "ascending",
            "sort_limit": 1,
        }
        brains = api.search(query, SAMPLE_CATALOG)
        year = brains[0].created.year()
        return datetime(year, 1, 1)

    def parse_date_to_output(self, date):
        return dtime.to_localized_time(date, long_format=False) or ""
