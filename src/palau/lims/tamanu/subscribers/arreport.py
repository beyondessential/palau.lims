# -*- coding: utf-8 -*-

from bika.lims import api
from palau.lims.tamanu import api as tapi
from palau.lims.tamanu.config import LOINC_CODING_SYSTEM
from palau.lims.tamanu.config import LOINC_GENERIC_DIAGNOSTIC
from palau.lims.tamanu.config import SENAITE_TESTS_CODING_SYSTEM
from palau.lims.utils import is_reportable
from senaite.core.api import dtime


def on_object_created(instance, event):
    """Event handler when a results report is created. Sends a POST back to
    the Tamanu instance for samples included in the report that have a Tamanu
    resource counterpart
    """
    # TODO decouple of events and do this thing in a script
    samples = instance.getContainedAnalysisRequests()
    for sample in samples:
        send_diagnostic_report(sample, instance)


def send_diagnostic_report(sample, report):
    """Notifies Tamanu instance back for this sample and report
    """
    # get the tamanu session
    session = tapi.get_tamanu_session_for(sample)
    if not session:
        return

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
    status = tapi.get_tamanu_status(sample, default="partial")

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
    # tamanu doesn't recognizes more than one coding, keep only the LOINC one
    coding = [dict(LOINC_GENERIC_DIAGNOSTIC)]
    panel = data.get("code") or {}
    for code in panel.get("coding") or []:
        if code.get("system") == LOINC_CODING_SYSTEM:
            coding = [code]
            break
    payload["code"] = {"coding": coding}

    # group the tests (orderDetails) requested by their original id
    ordered_tests_by_key = {}
    for order_detail in data.get("orderDetail", []):
        test = tapi.get_codings(order_detail, SENAITE_TESTS_CODING_SYSTEM)
        if test:
            key = test[0].get("code")
            ordered_tests_by_key[key] = order_detail

    # add the observations (analyses included in the results report)
    for analysis in sample.getAnalyses(full_objects=True):
        if not is_reportable(analysis):
            # skip non-reportable samples
            continue

        # get the original LabRequest's LOINC Code
        name = api.get_title(analysis)
        keyword = analysis.getKeyword()
        ordered_test = ordered_tests_by_key.get(keyword)
        if not ordered_test:
            ordered_test = ordered_tests_by_key.get(name, {"coding": []})

        # E.g. https://hl7.org/fhir/R4B/observation-example-f001-glucose.json.html
        observation = {
            "resourceType": "Observation",
            "status": tapi.get_tamanu_status(analysis),
            "code": ordered_test,
        }

        # quantitative / qualitative
        if analysis.getStringResult() or analysis.getResultOptions():
            # qualitative
            observation["valueString"] = analysis.getFormattedResult()
        else:
            # quantitative
            observation["valueQuantity"] = {
                "value": analysis.getResult(),
                "unit": analysis.getUnit(),
            }

        # append the observations
        payload.setdefault("results", []).append(observation)

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
