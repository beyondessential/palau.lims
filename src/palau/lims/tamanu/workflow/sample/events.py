# -*- coding: utf-8 -*-

from palau.lims.tamanu import api as tapi
from bika.lims import api
from palau.lims.tamanu.config import LOINC_CODING_SYSTEM
from senaite.core.api import dtime


def after_publish(sample):
    """Event fired after a sample gets published. Sends a POST back to the
    Tamanu instance if the sample has a Tamanu resource counterpart
    """
    # TODO Use arreport.on_create instead of sample.after_publish
    #      ARReport is the counterpart object for DiagnosisReport and it can
    #      have multiple samples on it (ContainedAnalysisRequests field). In
    #      fact, the status reported back to Tamanu is the status of the
    #      ARReport, not the status of the sample
    # do notify Tamanu only if a results report
    reports_ids = sample.objectIds("ARReport")
    if not reports_ids:
        return None

    # get the tamanu session
    session = tapi.get_tamanu_session_for(sample)
    if not session:
        return

    # get the last report
    report = sample.get(reports_ids[-1])

    # convert the uuid from hex to str
    report_uid = tapi.get_uuid(report)
    report_uid = str(report_uid)

    # get the original data
    meta = tapi.get_tamanu_storage(sample)
    data = meta.get("data") or {}

    # build the payload
    # TODO Add an adapter to build payloads for a given object (e.g ARReport)
    tamanu_uid = tapi.get_tamanu_uid(sample)
    modified = api.get_modification_date(sample)
    modified = dtime.to_iso_format(modified)
    payload = {
        # meta information about the DiagnosticReport (ARReport)
        "resourceType": "DiagnosticReport",
        "id": report_uid,
        "meta": {
            "lastUpdated": modified,
        },
        # the status of the DiagnosticReport (ARReport)
        "status": "final",
        # the ServiceRequest(s) this ARReport is based on
        # TODO What about a DiagnosticReport with more than one basedOn
        "basedOn": [{
            "type": "ServiceRequest",
            "reference": "ServiceRequest/{}".format(tamanu_uid),
        }],
        # Tamanu test panel info
        "code": data.get("code"),
        # tests that were requested that are included in this report
        "result": [],
    }

    # notify back to Tamanu
    # TODO Fix forbidden error when notifying back Tamanu with DiagnosticReport
    # {u'error': {u'status': 403, u'message': u'', u'name': u'ForbiddenError'}}
    session.post("DiagnosticReport", payload)
