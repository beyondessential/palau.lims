# -*- coding: utf-8 -*-

import argparse
from datetime import timedelta

from bika.lims import api
from bika.lims.interfaces import IClient
from bika.lims.interfaces import IContact
from palau.lims import logger
from palau.lims.scripts import setup_script_environment
from palau.lims.tamanu import api as tapi
from palau.lims.tamanu.session import TamanuSession

__doc__ = """
Import remote data from Tamanu
"""

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("--tamanu_host", "-th", help="Tamanu host")
parser.add_argument("--tamanu_credentials", "-tc", help="Tamanu user")


def get_client(resource):
    """Returns a client object counterpart for the given resource
    """
    client = resource.getObject()
    if not client:
        container = api.get_portal().clients
        return tapi.create_object(container, resource, portal_type="Client")
    if IClient.providedBy(client):
        return client
    raise TypeError("Object %s is not from Client type" % repr(client))


def get_contact(client, resource):
    """Returns a contact object counterpart for the given resource and client
    """
    contact = resource.getObject()
    if not contact:
        return tapi.create_object(client, resource, portal_type="Contact")
    if IContact.providedBy(contact):
        if api.get_parent(contact) == client:
            return contact
        raise TypeError("Contact %s does not belong to client %s")
    raise TypeError("Object %s is not from Contact type" % repr(contact))


def pull_and_sync(host, email, password):
    # start a remote session with tamanu
    session = TamanuSession(host)
    session.login(email, password)

    # get the service requests created/modified since 15d ago
    since = timedelta(days=-15)
    resources = session.get_resources("ServiceRequest", _lastUpdated=since)
    for service_request in resources:
        import pdb;pdb.set_trace()

        # check if a sample for this service_request exists already
        sample = service_request.getObject()
        if sample:
            # TODO update the sample with Tamanu's info
            continue

        # get or create the client via FHIR's encounter/serviceProvider
        resource = service_request.getServiceProvider()
        client = get_client(resource)

        # get or create the contact via FHIR's requester
        resource = service_request.getRequester()
        contact = get_contact(client, resource)

        # TODO what if the contact does not belong to same client?

        # get SampleType, Site and DateSampled via FHIR's specimen
        specimen_resource = service_request.getSpecimenResource()
        specimen = specimen_resource[0]
        sample_type = specimen.get_sample_type()
        site = specimen.get_site()
        date_sampled = specimen.get_date_sampled()

        # get or create the patient via FHIR's subject
        resource = service_request.getPatientResource()
        patient = resource.getObject()
        if not patient:
            container = api.get_portal().patients
            patient = tapi.create_object(container, resource)


def play(host, email, password):

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

    encounter = service_request.get("encounter")
    service_provider = encounter.get("serviceProvider")

    if service_provider:
        organization = service_request.get_reference(service_provider)
        org_name = organization.get("name")
        org_tamanu_uid = organization.get("id")
        client = service_request.search_by_uid(org_tamanu_uid)

        if not client:
            client = api.create(portal.clients, "Client", title=org_name)
            setattr(client, "tamanu_uid", org_tamanu_uid)
            client.reindexObject()

        # get the contact via FHIR's requester
        requester = service_request.get("requester")
        contact = service_request.search_by_uid(requester.get("id"))

        if not contact:
            name = requester.get("name")[0]
            name_text = name.get("text")
            contact_firstname, contact_lastname = name_text.split(" ", 1)
            contact = api.create(
                client, "Contact",
                Firstname=contact_firstname,
                Surname=contact_lastname
            )
            setattr(contact, "tamanu_uid", requester.get("id"))


    status = service_request.get("status")
    priority = service_request.get("priority")

    # get the raw returned information about the FHIR's requester
    contact = service_request.get_raw("requester")

    # get the raw returned information about the FHIR's requester
    contact = service_request.get_raw("subject")

    locations = encounter.get("location")

    # get the tests requested via FHIR's orderDetail
    tests = service_request.get("orderDetail")
    test_ids = [test["coding"][0]["code"] for test in tests]

    # Commit transaction
    logger.info("Commit transaction ...")
    #transaction.commit()
    logger.info("Commit transaction [DONE]")


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

    pull_and_sync(host, parts[0], parts[1])



if __name__ == "__main__":
    main(app)  # noqa: F821
