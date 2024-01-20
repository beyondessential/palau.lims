# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from palau.lims import messageFactory as _
from palau.lims.config import MONTHS
from palau.lims.reports import count_by
from palau.lims.reports import get_analyses_by_year
from palau.lims.reports import group_by
from palau.lims.reports.forms import CSVReport


class AnalysesLabDepartmentsByMonth(CSVReport):
    """Analyses Lab Departments by month
    """

    def process_form(self):
        # get the received samples within the given year
        year = int(self.request.form.get("year"))
        brains = get_analyses_by_year(year)

        # Group the analyses brains by sample type
        analyses_by_sample_types = group_by(brains, "getSampleTypeUID")

        # add the first row (header)
        months = [MONTHS[num] for num in range(1, 13)]
        rows = [[_("Lab Department")] + months + [_("Total For Year")]]

        # Group the analyses by departments
        analyses_by_lab_department = {}
        for sample_type, analyses in analyses_by_sample_types.items():
            for obj in analyses:
                analysis = api.get_object(obj)
                service_uids = analysis.getServiceUID()
                services = api.get_object(service_uids)
                department = services.getDepartment()
                if services.getDepartment():
                    department = api.get_title(department)
                else:
                    department = "Unknown"
                analyses_by_lab_department.setdefault(
                    department, []
                ).append(analysis)

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
