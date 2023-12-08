# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd


from collections import OrderedDict

from palau.lims import messageFactory as _
from palau.lims.reports import get_received_samples
from palau.lims.reports import group_by
from palau.lims.reports import count_by
from palau.lims.reports.forms import CSVReport


class SamplesReceivedByDepartment(CSVReport):
    """Samples received by department
    """

    def process_form(self):
        from_date = self.request.form.get("date_from")
        to_date = self.request.form.get("date_to")
        query = {
            "review_state": "published",
        }
        brains = get_received_samples(from_date, to_date, **query)
        sample_types = list(OrderedDict.fromkeys(sorted(map(lambda brain: brain.getSampleTypeTitle, brains))))
        samples_by_dept = group_by(brains, "getWardDepartment")

        rows = []
        for dept, samples_in_dept in samples_by_dept.items():
            counted_samples_by_sample_type = count_by(samples_in_dept, "getSampleTypeTitle")
            row = [dept]
            for sample_type in sample_types:
                value = counted_samples_by_sample_type[sample_type] if sample_type in counted_samples_by_sample_type else 0
                row.append(value)
            rows.append(row)

        header_sample_types = [title for title in sample_types]
        headers = [_("Department")] + header_sample_types
        rows.insert(0, headers)

        return rows