# -*- coding: utf-8 -*-

from palau.lims.tamanu import api as tapi
from bika.lims import api
from senaite.core.api import dtime


def after_publish(sample):
    """Event fired after a sample gets published. Sends a POST back to the
    Tamanu instance if the sample has as Tamanu resource counterpart
    """
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

    # build the payload
    tamanu_uid = tapi.get_tamanu_uid(sample)
    modified = api.get_modification_date(sample)
    modified = dtime.to_iso_format(modified)
    payload = {
        "resourceType": "DiagnosticReport",
        "id": report_uid,
        "meta": {
            "lastUpdated": modified,
        },
        "status": "final",
        "basedOn": [{
            "type": "ServiceRequest",
            "reference": "ServiceRequest/{}".format(tamanu_uid),
        }],
    }

    # notify back to Tamanu
    # TODO I get a forbidden error:
    # {u'error': {u'status': 403, u'message': u'', u'name': u'ForbiddenError'}}
    session.post("DiagnosticReport", payload)
