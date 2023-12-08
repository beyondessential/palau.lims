# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd


from palau.lims import messageFactory as _
from palau.lims.config import MONTHS
from palau.lims.reports import count_by
from palau.lims.reports import get_received_samples_by_year
from palau.lims.reports import group_by
from palau.lims.reports.forms import CSVReport


class SamplesReceivedByMonth(CSVReport):
    """Samples received by month
    """

    def process_form(self):
        year = int(self.request.form.get("year"))
        brains = get_received_samples_by_year(year)
        samples_by_sample_type = group_by(brains, "getSampleTypeTitle")

        rows = []
        for sample_type, samples_in_sample_type in samples_by_sample_type.items():
            counted_samples_by_month = count_by(samples_in_sample_type, "getDateReceived")
            row = [sample_type]
            for month in range(1, 13):
                value = counted_samples_by_month[month] if month in counted_samples_by_month else 0
                row.append(value)
            rows.append(row)

        header_months = [MONTHS[num] for num in range(1, 13)]
        header = [_("Sample type")] + header_months
        rows.insert(0, header)

        return rows