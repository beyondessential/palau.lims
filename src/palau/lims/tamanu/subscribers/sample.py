# -*- coding: utf-8 -*-

from palau.lims.tamanu.subscribers.arreport import send_diagnostic_report


def on_after_transition(sample, event):  # noqa camelcase
    """Actions to be done when a transition for a sample takes place
    """
    if not event.transition:
        return

    # get the last report for this sample, if any
    report = get_last_report(sample)

    # notify tamanu back about this report status
    send_diagnostic_report(sample, report)


def get_last_report(sample):
    """Returns the last analysis report that was created for this sample
    """
    reports_ids = sample.objectIds("ARReport")
    if not reports_ids:
        return None
    return sample.get(reports_ids[-1])
