# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from palau.lims import messageFactory as _
from palau.lims.config import MONTHS
from palau.lims.reports import count_by
from palau.lims.reports import get_received_samples_by_year
from palau.lims.reports import get_reportable_analyses
from palau.lims.reports.forms import CSVReport


class AnalysesLabDepartmentsByMonth(CSVReport):
    """Analyses Lab Departments by month
    """

    def process_form(self):
        # get the received samples within the given year
        year = int(self.request.form.get("year"))
        brains = get_received_samples_by_year(year)

        # add the first row (header)
        months = [MONTHS[num] for num in range(1, 13)]
        rows = [[_("Lab Department")] + months + [_("Total For Year")]]

        samples = map(api.get_object, brains)
        samples_analyses = get_reportable_analyses(samples)

        # group the analyses by departments
        analyses_by_lab_department = {}
        for analysis in samples_analyses:
            service_uids = analysis.getServiceUID()
            services = api.get_object(service_uids)
            department = services.getDepartment()
            department = api.get_title(department) if department else "Unknown"
            analyses_by_lab_department.setdefault(department, []).append(analysis)

        # sort departments alphabetically ascending
        lab_departments = sorted(analyses_by_lab_department.keys())

        for lab_department in lab_departments:
            # group and count the analyses by reception date
            analyses = analyses_by_lab_department[lab_department]
            counts = count_by(analyses, "getDateReceived")

            # get the analysis count for each registered month
            analysis_counts = map(lambda mth: counts.get(mth, 0), range(1, 13))
            # build the row
            rows.append(
                [lab_department] + analysis_counts + [sum(analysis_counts)]
            )

        return rows
