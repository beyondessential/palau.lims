# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from datetime import datetime
from plone.memoize import view
from palau.lims.config import TARGET_PATIENTS
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as PT
from senaite.core.catalog import SAMPLE_CATALOG

YEAR_CONTROL = "controls/year.pt"
DATE_CONTROL = "controls/date.pt"
TARGET_PATIENT_CONTROL = "controls/target_patient.pt"


class StatisticReportsView(BrowserView):
    """Statistics view form
    """
    template = PT("templates/statistic_reports.pt")

    def __call__(self):
        form = self.request.form

        submit = form.get("submit")
        report_id = form.get("report_id")

        if submit and report_id:
            report_form = api.get_view(report_id)
            return report_form()

        return self.template()

    def year_control(self):
        """Returns the control for year selection
        """
        return PT(YEAR_CONTROL)(self)

    def date_control(self):
        """Returns the control for date selection
        """
        return PT(DATE_CONTROL)(self)

    def target_patient_control(self):
        """Returns the control for year selection
        """
        return PT(TARGET_PATIENT_CONTROL)(self)

    @view.memoize
    def get_years(self):
        """Returns the list of years since the first sample was created
        """
        query = {
            "portal_type": "AnalysisRequest",
            "sort_on": "created",
            "sort_order": "ascending",
            "sort_limit": 1,
        }

        since = datetime.now().year
        brains = api.search(query, SAMPLE_CATALOG)
        if brains:
            since = brains[0].created.year()

        current = datetime.now().year
        return range(since, current+1)

    def get_target_patients(self):
        """Returns the list target patient
        """
        return TARGET_PATIENTS

    def render_report_section(self, report_id):
        """Renders the report section with the given id
        """
        template_path = "templates/{}.pt".format(report_id)
        template = PT(template_path)
        return template(self)

    @property
    def date_from(self):
        """Returns the first date of selected duration
        """
        # Default to first day of current month
        default = datetime.now()
        default = datetime(default.year, default.month, 1)
        date_from = self.request.form.get("date_from", None)
        date_from = api.to_date(date_from, default=default)
        return date_from.strftime("%Y-%m-%d")

    @property
    def date_to(self):
        """Returns the last date of selected duration
        """
        date_to = self.request.form.get("date_to", None)
        date_to = api.to_date(date_to, default=datetime.now())
        return date_to.strftime("%Y-%m-%d")
