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
        # get the rejected samples within the period
        dt_from = self.request.form.get("date_from")
        dt_to = self.request.form.get("date_to")
        brains = get_received_samples(dt_from, dt_to, review_state="rejected")

        # generate the rows
        rows = map(self.to_row, brains)

        # insert the first row (header)
        header = [
            _("Sample ID"),
            _("Client Name"),
            _("Referring Doctor"),
            _("Sample Type"),
            _("Sample Received Date"),
            _("Sample Rejection Date"),
            _("Reason For Rejection"),
        ]
        rows.insert(0, header)
        return rows

    def to_row(self, sample):
        """Returns a row representing the sample passed-in
        """
        sample = api.get_object(sample)

        # Reasons for rejection
        reasons = ", ".join(sample.getSelectedRejectionReasons())
        other = sample.getOtherRejectionReasons()
        if other:
            reasons = reasons + ", " + other if reasons else other

        return [
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
            reasons,
        ]
