# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

import re

from bika.lims import api

from palau.lims import messageFactory as _
from palau.lims.reports import get_analyses_by_result_category_department
from palau.lims.reports.forms import CSVReport
from palau.lims.utils import get_field_value

INT_RE = re.compile(r"\d+")
SEX_CAST = {
    "m": "male",
    "f": "female",
}

class AnalysesResults(CSVReport):
    """Analyses Lab Departments by month
    """

    def process_form(self):
        # verified and published samples that were received within a given year
        statuses = ["verified", "published"]

        # Filter the analyses per result, category and department
        resultText = self.request.form.get("result") or None
        category = self.request.form.get("category") or None
        department = self.request.form.get("department") or None

        brains = get_analyses_by_result_category_department(
            resultText, category, department, review_state=statuses
        )

        # add the first row (header)
        rows = [[
            _("Analysis Title"),
            _("Analysis Request ID"),
            _("Analysis ID"),
            _("Analysis Category"),
            _("Analysis Department"),
            _("Patient Name"),
            _("Patient Surname"),
            _("Patient Other Names"),
            _("Patient Hospital #"),
            _("Patient Date of Birth"),
            _("Patient Gender"),
            _("Test Date Collected"),
            _("Test Date Tested"),
            _("Test Type"),
            _("Test Result"),
            _("Site"),
            _("Requesting Physician"),
        ]]

        for brain in brains:
            analysis = api.get_object(brain)
            sample = analysis.getRequest()
            patient_name = get_field_value(sample, "PatientFullName", default={})
            mrn = get_field_value(sample, "MedicalRecordNumber", default={})
            mrn = mrn.get("value", "")

            if not resultText:
                result_matches = INT_RE.search(analysis.getResult())
                result = result_matches.group(0) if result_matches else ''
                for option in analysis.getResultOptions():
                    if option["ResultText"] == resultText and option["ResultValue"] == result:
                        resultText = option["ResultText"]
                        break

            if not department:
                department = analysis.getDepartment()

            category = category or analysis.getCategoryTitle() or ""

            # add the info for each analysis in a row
            rows.append(
                [
                    analysis.Title() or "",
                    analysis.getRequestID() or "",
                    analysis.getId() or "",
                    category,
                    department.Title() if department else "",
                    patient_name.get("firstname", ""),
                    patient_name.get("lastname", ""),
                    patient_name.get("middlename", ""),
                    mrn or "",
                    sample.getDateOfBirth()[0] or "",
                    SEX_CAST.get(sample.getSex(), ""),
                    sample.getDateSampled() or "",
                    analysis.getResultCaptureDate() or "",
                    sample.getSampleTypeTitle() or "",
                    resultText or "",
                    sample.getClientTitle() or "",
                    sample.getContactFullName() or "",
                ]
            )

        return rows
