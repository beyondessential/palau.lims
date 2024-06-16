# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.core.api import dtime
from palau.lims.tamanu import api as tapi


SAMPLE_TRANSITIONS = (
    # mapping between senaite actions and tamanu statuses
    ("cancel", "revoked"),
    ("reject", "revoked"),
    ("invalidate", "entered-in-error")
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
    modified = api.get_modification_date(sample)
    modified = dtime.to_iso_format(modified)
    payload = {
        "resourceType": "ServiceRequest",
        "id": tamanu_uid,
        "meta": {
            "lastUpdated": modified,
        },
        "status": status,
    }

    # notify tamanu
    session.post("ServiceRequest", payload)
