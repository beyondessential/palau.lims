# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from palau.lims import messageFactory as _
from palau.lims.reports import count_by
from palau.lims.reports import calculate_rate
from palau.lims.reports import get_received_samples_by_year
from palau.lims.reports.forms import CSVReport


class SamplesRejectionRateBySpecimenType(CSVReport):
    """Samples rejected by Specimen
    """

    def process_form(self):
        year = int(self.request.form.get("year"))

        # get received and rejected samples
        received = get_received_samples_by_year(year)
        rejected = get_received_samples_by_year(year, review_state="rejected")

        # get the sample types
        sample_types = map(lambda brain: brain.getSampleTypeTitle, received)
        sample_types = sorted(list(set(sample_types)))

        count_received = count_by(received, "getSampleTypeTitle")
        count_rejected = count_by(rejected, "getSampleTypeTitle")

        rows = []
        row_received = [_("Total samples received")]
        row_rejected = [_("Total samples rejected")]
        row_rate = [_("Sample rejection rate (%)")]
        for sample_type in sample_types:
            num_received = count_received.get(sample_type, 0)
            num_rejected = count_rejected.get(sample_type, 0)
            rejection_rate = calculate_rate(num_received, num_rejected)

            row_received.append(num_received)
            row_rejected.append(num_rejected)
            row_rate.append(rejection_rate)

        rows.extend([row_received, row_rejected, row_rate])

        headers = [""] + sample_types
        rows.insert(0, headers)
        return rows
