# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from bes.lims.impress.reportview import DefaultReportView as BaseView


class DefaultReportView(BaseView):
    """Product-specific controller view for Palau results reports
    """

    def get_department(self, sample):
        """Returns the Department title
        """
        sample = api.get_object(sample)
        department = sample.getWardDepartment()
        if not department:
            return ""
        return api.get_title(department)

    def is_out_of_stock(self, analysis):
        """Returns whether the analysis passed-in is out-of-stock
        """
        return api.get_review_status(analysis) == "out_of_stock"
