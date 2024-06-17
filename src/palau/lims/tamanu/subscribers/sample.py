# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.core.api import dtime
from palau.lims.tamanu import api as tapi


SAMPLE_TRANSITIONS = (
    # mapping between senaite actions and tamanu statuses
    ("cancel", "cancelled"),
    ("reject", "cancelled"),
    ("publish", "final"),
    ("invalidate", "entered-in-error"),
)


def on_after_transition(sample, event):  # noqa camelcase
    """Actions to be done when a transition for a sample takes place
    """
    if not event.transition:
        return

    action = event.transition.id
    status = dict(SAMPLE_TRANSITIONS).get(action)
    if not status:
        return

    # get the tamanu session
    session = tapi.get_tamanu_session_for(sample)
    if not session:
        return

    # report back to Tamanu
    tamanu_uid = tapi.get_tamanu_uid(sample)
    
    # convert the uuid from hex to str
    report_uid = tapi.get_uuid(sample)
    report_uid = str(report_uid)
    
    modified = api.get_modification_date(sample)
    modified = dtime.to_iso_format(modified)
    payload = {
        "resourceType": "DiagnosticReport",
        "id": report_uid,
        "meta": {
            "lastUpdated": modified,
        },
        "status": status,
        "basedOn": [{
            "type": "ServiceRequest",
            "reference": "ServiceRequest/{}".format(tamanu_uid)}
        ],
        "code": {
            "coding": [{
              "system": "http://loinc.org",
              "code": "30954-2",
              "display": "Relevant diagnostic tests/laboratory data Narrative"
            }]
        }
    }

    # notify tamanu
    session.post("ServiceRequest", payload)
