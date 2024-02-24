# -*- coding: utf-8 -*-

import argparse
from datetime import timedelta
from bika.lims import api
from palau.lims.scripts import setup_script_environment
from palau.lims.tamanu.session import TamanuSession

__doc__ = """
Import remote data from Tamanu
"""

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("--tamanu_host", "-th", help="Tamanu host")
parser.add_argument("--tamanu_credentials", "-tc", help="Tamanu user")


def play(host, email, password):

    import pdb;pdb.set_trace()
    portal = api.get_portal()
    # start a remote session with tamanu
    session = TamanuSession(host)
    session.login(email, password)

    # get the service requests created/modified since 15d ago
    since = timedelta(days=-15)
    resources = session.get_resources("ServiceRequest", _lastUpdated=since)

    # inspect the first service request
    # get the available keys
    service_request = resources[0]
    request_id = service_request.get("id")

    organization = service_request.get("serviceProvider")
    # organization = {
    #     u'display': u'Facility 1', u'id': u'b451d7dc-746b-4203-afcb-7c695ca4a743'
    # }

    org_name = organization.get("display")
    org_tamanu_uid = organization.get("id")
    client = service_request.search("serviceProvider")

    if not client:
        client = api.create(portal.clients, "Client", title=org_name)
        setattr(client, "tamanu_uid", org_tamanu_uid)
        client.reindexObject()

    status = service_request.get("status")
    priority = service_request.get("priority")

    # get the raw returned information about the FHIR's requester
    contact = service_request.get_raw("requester")

    # get the contact via FHIR's requester
    contact = service_request.get("requester")

    # get the raw returned information about the FHIR's requester
    contact = service_request.get_raw("subject")

    # get the patient via FHIR's subject
    patient = service_request.get("subject")

    # get the ward? via FHIR's encounter
    encounter = service_request.get("encounter")
    locations = encounter.get("location")

    # get the tests requested via FHIR's orderDetail
    tests = service_request.get("orderDetail")
    test_ids = [test["coding"][0]["code"] for test in tests]



def main(app):
    args, _ = parser.parse_known_args()

    # get the remote host
    host = args.tamanu_host
    if not host:
        print("Remote URL is missing")
        return

    # get the user and password
    credentials = args.tamanu_credentials or ""
    parts = credentials.split(":")
    if len(parts) < 2:
        print("User and/or password are missing")
        return

    # Setup environment
    setup_script_environment(app)

    play(host, parts[0], parts[1])



if __name__ == "__main__":
    main(app)  # noqa: F821
