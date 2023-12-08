# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class StatisticReportsView(BrowserView):
    """Statistic view form
    """
    template = ViewPageTemplateFile("templates/statistic_reports.pt")

    def __call__(self):
        return self.template()