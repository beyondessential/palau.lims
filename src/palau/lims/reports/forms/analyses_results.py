# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from bika.lims import api

from palau.lims import messageFactory as _
from palau.lims.reports import get_analyses_by_result_category_department
from palau.lims.reports.forms import CSVReport
from palau.lims.utils import get_field_value

SEX_CAST = {
    "m": "Male",
    "f": "Female",
}


class AnalysesResults(CSVReport):
    """Analyses by result, category and department
    """

    def process_form(self):
        # Always filter analyses by verified and published in this form
        statuses = ["verified", "published"]

        # Collect the analyses filters (result, category and department)
        resultText = self.request.form.get("result") or None
        category = self.request.form.get("category") or None
        department = self.request.form.get("department") or None

        # Get the filtered analyses list
        brains = get_analyses_by_result_category_department(
            resultText, category, department, review_state=statuses
        )

        # Add the first row (header)
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

        # Add the info per analysis in a row
        for brain in brains:
            analysis = api.get_object(brain)

            sample = analysis.getRequest()
            patient_name = get_field_value(
                sample, "PatientFullName", default={}
            )
            mrn = get_field_value(sample, "MedicalRecordNumber", default={})
            mrn = mrn.get("value", "")

            resultText = resultText or analysis.getFormattedResult() or  ""
            department = department or analysis.getDepartmentTitle() or  ""
            category = category or analysis.getCategoryTitle() or  ""

            # add the info for each analysis in a row
            rows.append(
                [
                    analysis.Title(),
                    analysis.getRequestID(),
                    analysis.getId(),
                    category,
                    department,
                    patient_name.get("firstname", ""),
                    patient_name.get("lastname", ""),
                    patient_name.get("middlename", ""),
                    mrn,
                    sample.getDateOfBirth()[0] or "",
                    SEX_CAST.get(sample.getSex(), ""),
                    sample.getDateSampled() or "",
                    analysis.getResultCaptureDate() or "",
                    sample.getSampleTypeTitle() or "",
                    resultText,
                    sample.getClientTitle() or "",
                    sample.getContactFullName() or "",
                ]
            )

        return rows
