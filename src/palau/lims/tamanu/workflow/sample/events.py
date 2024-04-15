# -*- coding: utf-8 -*-

from palau.lims.tamanu import api as tapi
from bika.lims import api
from senaite.core.api import dtime


def after_republish(sample):
    """Event fired after a Sample is republished
    """
    after_republish(sample)


def after_prepublish(sample):
    """Event fired after a Sample is pre-published
    """
    after_publish(sample)


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

    # handle the status to report back to Tamanu
    # registered | partial | preliminary | final
    sample_status = api.get_review_status(sample)
    if sample_status == "published":
        # TODO status 'final' only if all requested analyses were included in
        #      the ARReport. Otherwise, 'partial'
        status = "final"
    elif sample_status in ["verified", "to_be_verified"]:
        status = "preliminary"
    else:
        status = "registered"

    payload = {
        # meta information about the DiagnosticReport (ARReport)
        "resourceType": "DiagnosticReport",
        "id": report_uid,
        "meta": {
            "lastUpdated": modified,
        },
        # the status of the DiagnosticReport (ARReport)
        # registered | partial | preliminary | final
        "status": status,
        # the ServiceRequest(s) this ARReport is based on
        # TODO What about a DiagnosticReport with more than one basedOn
        "basedOn": [{
            "type": "ServiceRequest",
            "reference": "ServiceRequest/{}".format(tamanu_uid),
        }],
    }

    # add the test panel (profile) if set or use LOINC's generic
    panel = data.get("code") or {}
    coding = panel.get("coding") or []
    if not coding:
        # Use generic LOINC code 30954-2 (https://loinc.org/30954-2)
        coding = [{
            "system": "http://loinc.org",
            "code": " 30954-2",
            "display": "Relevant Dx tests/lab data"
        }]

    # attach the pdf encoded in base64
    pdf = report.getPdf()
    coding[0].update({
        "data": pdf.data.encode("base64"),
        "contentType": "application/pdf",
    })
    payload["code"] = {"coding": coding}

    # notify back to Tamanu
    # TODO Fix forbidden error when notifying back Tamanu with DiagnosticReport
    # {u'error': {u'status': 403, u'message': u'', u'name': u'ForbiddenError'}}
    session.post("DiagnosticReport", payload)
