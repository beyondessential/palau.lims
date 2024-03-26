# -*- coding: utf-8 -*-

import argparse
import transaction
from bika.lims import api
from bika.lims.interfaces import IClient
from bika.lims.interfaces import IContact
from bika.lims.utils.analysisrequest import \
    create_analysisrequest as create_sample
from datetime import timedelta
from palau.lims import logger
from palau.lims.scripts import setup_script_environment
from palau.lims.tamanu import api as tapi
from palau.lims.tamanu.session import TamanuSession
from senaite.patient.interfaces import IPatient
from senaite.core.catalog import SETUP_CATALOG

__doc__ = """
Import remote data from Tamanu
"""

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("--tamanu_host", "-th", help="Tamanu host")
parser.add_argument("--tamanu_credentials", "-tc", help="Tamanu user")
parser.add_argument("--since", "-s", help="Last updated since (days)")
parser.add_argument("--dry", "-d", help="Run in dry mode")

# Service Request statuses to skip
SKIP_STATUSES = ["revoked", "draft", "entered-in-error"]

# Priorities mapping
PRIORITIES = (
    ("routine", "5"),
    ("urgent", "3"),
    ("asap", "3"),
    ("stat", "1"),
)


def get_client(service_request):
    """Returns a client object counterpart for the given resource
    """
    resource = service_request.getServiceProvider()
    client = resource.getObject()
    if not client:
        container = api.get_portal().clients
        return tapi.create_object(container, resource, portal_type="Client")
    if IClient.providedBy(client):
        return client
    raise TypeError("Object %s is not from Client type" % repr(client))


def get_contact(service_request):
    """Returns a contact object counterpart for the given resource and client
    """
    # get the client
    client = get_client(service_request)
    # get the contact
    resource = service_request.getRequester()
    contact = resource.getObject()
    if not contact:
        return tapi.create_object(client, resource, portal_type="Contact")
    if IContact.providedBy(contact):
        if api.get_parent(contact) == client:
            return contact
        raise TypeError("Contact %s does not belong to client %s" % (
            repr(contact), repr(client)))
    raise TypeError("Object %s is not from Contact type" % repr(contact))


def get_patient(service_request):
    """Returns a patient object counterpart for the given resource
    """
    resource = service_request.getPatientResource()
    patient = resource.getObject()
    if not patient:
        container = api.get_portal().patients
        return tapi.create_object(container, resource, portal_type="Patient")
    if IPatient.providedBy(patient):
        return patient
    raise TypeError("Object %s is not from Patient type" % repr(patient))


def get_sample_type(service_request):
    """Returns a sample type counterpart for the given resource
    """
    specimen = service_request.getSpecimen()
    sample_type = specimen.get_sample_type()
    if sample_type:
        return sample_type

    info = specimen.get_sample_type_info()
    if not info:
        raise ValueError("Sample type is missing: %s" % repr(specimen))

    # TODO QA We create the sample type if no matches are found!
    title = info.get("title")
    if not title:
        raise ValueError("Sample type without title: %s" % repr(specimen))

    container = api.get_setup().bika_sampletypes
    return api.create(container, "SampleType", **info)


def get_sample_point(service_request):
    """Returns a sample type counterpart for the given resource if defined
    """
    specimen = service_request.getSpecimen()
    sample_point = specimen.get_sample_point()
    if sample_point:
        return sample_point

    info = specimen.get_sample_point_info()
    if not info:
        # Sample point is not a required field
        return None

    # TODO QA We create the sample point if no matches are found!
    title = info.get("title")
    if not title:
        raise ValueError("Sample point without title: %s" % repr(specimen))

    container = api.get_setup().bika_samplepoints
    return api.create(container, "SamplePoint", **info)


def get_services(service_request):
    """Returns the service objects counterpart for the given resource
    """
    # TODO Implement
    details = service_request.get("orderDetail")
    keywords = set()
    for detail in details:
        keyword = detail.get("text")
        keywords.add(keyword)

    keywords = list(keywords)
    if not keywords:
        return []

    query = {
        "portal_type": "AnalysisService",
        "is_active": True,
        "getKeyword": list(keywords)
    }
    brains = api.search(query, SETUP_CATALOG)
    return map(api.get_object, brains)


def pull_and_sync(host, email, password, since=15, dry_mode=True):
    # start a remote session with tamanu
    session = TamanuSession(host)
    session.login(email, password)

    # get the service requests created/modified since?
    since = timedelta(days=-since)
    resources = session.get_resources("ServiceRequest", _lastUpdated=since)
    for sr in resources:

        # get the Tamanu's test ID for this ServiceRequest
        lab_test_id = sr.getLabTestID()

        # check if a sample for this service_request exists already
        sample = sr.getObject()
        if sample:
            # TODO update the sample with Tamanu's info
            logger.info("----> TO UPDATE: %s" % repr(sample))
            continue

        if sr.status in SKIP_STATUSES:
            logger.info("Skip (status=%s): %s" % (sr.status, repr(sr)))
            continue

        # get SampleType, Site and DateSampled via FHIR's specimen
        specimen = sr.getSpecimen()
        if not specimen:
            logger.error("No specimen: %s" % repr(sr))
            continue

        # get the sample type
        sample_type = get_sample_type(sr)

        # get the sample point
        sample_point = get_sample_point(sr)

        # date sampled
        date_sampled = specimen.get_date_sampled()

        # get the priority and others
        priority = sr.get("priority")
        priority = dict(PRIORITIES).get(priority, "5")

        # get or create the client via FHIR's encounter/serviceProvider
        client = get_client(sr)

        # get or create the contact via FHIR's requester
        contact = get_contact(sr)

        # get or create the patient via FHIR's subject
        patient = get_patient(sr)
        patient_mrn = patient.getMRN()
        patient_dob = patient.getBirthdate()
        patient_sex = patient.getSex()
        patient_name = {
            "firstname": patient.getFirstname(),
            "middlename": patient.getMiddlename(),
            "lastname": patient.getLastname(),
        }

        # create the sample
        services = get_services(sr)
        values = {
            "Client": client,
            "Contact": contact,
            "SampleType": sample_type,
            # TODO SamplePoint field is disabled, we used Site instead
            "SamplePoint": sample_point,
            "Site": sample_point,
            "DateSampled": date_sampled,
            "Template": None,
            "Profiles": [],
            "MedicalRecordNumber": {"value": patient_mrn},
            "PatientFullName": patient_name,
            "DateOfBirth": patient_dob,
            "Sex": patient_sex,
            "Priority": priority,
            "ClientSampleID": lab_test_id,
            #"Ward": api.get_uid(ward),
            #"ClinicalInformation": "",
            #"DateOfAdmission": doa,
            #"CurrentAntibiotics": antibiotics,
            #"Volume": volume,
            #"WardDepartment": department,
            #"Location": dict(LOCATIONS).get("location", ""),
            #"Site": api.get_uid(sample_point) if sample_point else "",
        }
        request = api.get_request() or api.get_test_request()
        sample = create_sample(client, request, values, services)
        # link the tamanu resource to this sample
        tapi.link_tamanu_resource(sample, sr)
        logger.info("Object created: %s" % repr(sample))

    if dry_mode:
        # Dry mode. Do not do transaction
        return

    # Commit transaction
    logger.info("Commit transaction ...")
    transaction.commit()
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

    # get since days
    since = api.to_int(args.since, default=5)

    # dry mode
    trues = ["True", "true", "1", "yes", "y"]
    dry = args.dry in trues

    # Setup environment
    setup_script_environment(app, stream_out=False)

    pull_and_sync(host, parts[0], parts[1], since=since, dry_mode=dry)


if __name__ == "__main__":
    main(app)  # noqa: F821
