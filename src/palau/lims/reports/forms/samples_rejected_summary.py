# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd


from bika.lims import api
from bika.lims.browser import ulocalized_time
from bika.lims.workflow import getTransitionDate
from palau.lims import messageFactory as _
from palau.lims.reports import get_received_samples
from palau.lims.reports.forms import CSVReport


class SamplesRejectedSummary(CSVReport):
    """Samples rejected summary
    """

    def process_form(self):
        from_date = self.request.form.get("date_from")
        to_date = self.request.form.get("date_to")
        query = {
            "review_state": "rejected",
        }
        rejected_brains = get_received_samples(from_date, to_date, **query)
        rejected_samples = map(api.get_object, rejected_brains)

        # Build the rows
        rows = []
        for sample in rejected_samples:
            rows.append([
                sample.getId(),
                sample.getClientTitle(),
                sample.getContactFullName(),
                sample.getSampleTypeTitle(),
                ulocalized_time(
                    sample.getDateReceived(),
                    long_format=True,
                    time_only=False, context=sample
                ),
                getTransitionDate(sample, 'reject'),
                ", ".join(sample.getSelectedRejectionReasons()),
            ])

        # Prepare the header
        headers = [
            _("Sample ID"),
            _("Client Name"),
            _("Referring Doctor"),
            _("Sample Type"),
            _("Sample Received Date"),
            _("Sample Rejection Date"),
            _("Reason For Rejection"),
        ]
        rows.insert(0, headers)
        return rows