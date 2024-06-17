# -*- coding: utf-8 -*-

import argparse
from datetime import timedelta

import transaction
from bika.lims import api
from bika.lims.api import security as sapi
from bika.lims.interfaces import IClient
from bika.lims.interfaces import IContact
from bika.lims.utils.analysisrequest import \
    create_analysisrequest as create_sample
from bika.lims.workflow import doActionFor
from palau.lims.config import TAMANU_ID
from palau.lims.scripts import setup_script_environment
from palau.lims.tamanu import api as tapi
from palau.lims.tamanu import logger
from palau.lims.tamanu.config import SAMPLE_FINAL_STATUSES
from palau.lims.tamanu.config import SENAITE_PROFILES_CODING_SYSTEM
from palau.lims.tamanu.config import SENAITE_TESTS_CODING_SYSTEM
from palau.lims.tamanu.session import TamanuSession
from Products.CMFCore.permissions import ModifyPortalContent
from senaite.core.catalog import SETUP_CATALOG
from senaite.patient import api as papi
from senaite.patient.interfaces import IPatient

__doc__ = """
Import and sync Tamanu resources
Imports existing resources from Tamanu server and creates them in SENAITE. They
are updated accordingly if already exists in SENAITE.
"""

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument(
    "-th", "--tamanu_host",
    help="URL from the Tamanu instance to extract the data from"
)
parser.add_argument(
    "-tu", "--tamanu_user",
    help="User and password in the <username>:<password> form"
)
parser.add_argument(
    "-r", "--resource",
    help="Resource type to sync. Supported: Patient, ServiceRequest"
)
parser.add_argument(
    "-s", "--since",
    help="Last updated since (days)"
)
parser.add_argument(
    "-d", "--dry",
    help="Run in dry mode"
)

SKIP_STATUSES = (
    # Service Request statuses to skip
    "revoked", "draft", "entered-in-error"
)

TRANSITIONS = (
    # Tuples of (tamanu status, transition)
    ("revoked", "cancel"),
    ("entered-in-error", "reject"),
)

# Priorities mapping
PRIORITIES = (
    ("stat", "1"),
    ("asap", "3"),
    ("routine", "5"),
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


def get_patient(resource):
    """Returns a patient object counterpart for the given resource
    """
    patient = resource.getObject()
    if not patient:

        # TODO QA patient not linked to this resource but same MRN exists
        mrn = resource.get_mrn()
        if not mrn:
            raise ValueError("Patient without MRN (ID): %s" % repr(resource))

        patient = papi.get_patient_by_mrn(mrn, include_inactive=True)
        if patient:
            # link the resource to this Patient object
            tapi.link_tamanu_resource(patient, resource)
            return patient

        # Create a new patient
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

    container = api.get_senaite_setup().samplepoints
    return api.create(container, "SamplePoint", **info)


def get_services(service_request):
    """Returns the service objects counterpart for the given resource
    """
    services = []

    # get all services and group them by title
    by_title = {}
    by_keyword = {}
    sc = api.get_tool(SETUP_CATALOG)
    for brain in sc(portal_type="AnalysisService"):
        obj = api.get_object(brain)
        by_title[api.get_title(obj)] = obj
        by_keyword[obj.getKeyword()] = obj

    # get the codes requested in the ServiceRequest
    details = service_request.get("orderDetail")
    for coding in tapi.get_codings(details, SENAITE_TESTS_CODING_SYSTEM):
        # get the analysis by keyword
        code = coding.get("code")
        service = by_keyword.get(code)
        if not service:
            # fallback to title
            # TODO Fallback searches by analysis to CommercialName instead?
            display = coding.get("display")
            service = by_title.get(display)

        if service:
            services.append(service)

    return services


def get_profiles(service_request):
    """Returns the profile objects counterpart for the given resource
    """
    profiles = []

    # get all profiles and group them by profile key and title
    by_title = {}
    by_keyword = {}
    sc = api.get_tool(SETUP_CATALOG)
    for brain in sc(portal_type="AnalysisProfile"):
        obj = api.get_object(brain)
        by_title[api.get_title(obj)] = obj
        key = obj.getProfileKey()
        if key:
            by_keyword[key] = obj

    # get the profile codes requested in the ServiceRequest
    codings = service_request.get("code")
    for coding in tapi.get_codings(codings, SENAITE_PROFILES_CODING_SYSTEM):
        # get the profile by keyword
        code = coding.get("code")
        profile = by_keyword.get(code)
        if not profile:
            # fallback to title
            # TODO Fallback searches by analysis to CommercialName instead?
            display = coding.get("display")
            profile = by_title.get(display)

        if profile:
            profiles.append(profile)

    return profiles


def get_remarks(service_request):
    """Returns the Remarks counterpart for the given resource
    """
    remarks = []
    notes = service_request.get("note") or []
    for note in notes:
        item = {
            "user_id": "tamanu",
            "user_name": "Tamanu",
            "created": note.get("time"),
            "content": note.get("text")
        }
        remarks.append(item)
    return remarks


def sync_patients(session, since=15, dry_mode=True):
    # get the patients created/modified since?
    since = timedelta(days=-since)
    resources = session.get_resources(
        "Patient", _lastUpdated=since, active="true"
    )
    total = len(resources)
    for num, resource in enumerate(resources):
        if num and num % 100 == 0:
            logger.info("Processing patients {}/{}".format(num, total))

        mrn = resource.get_mrn() or "unk"
        logger.info("Processing Patient '{}' ({})".format(mrn, resource.UID))

        # get/create the patient
        patient = get_patient(resource)

        # update the patient
        values = resource.to_object_info()
        api.edit(patient, check_permissions=False, **values)

        # assign ownership to 'tamanu' user
        creator = patient.Creator()
        if creator != TAMANU_ID:
            sapi.revoke_local_roles_for(patient, roles=["Owner"], user=creator)

        # grant 'Owner' role to the user who is modifying the object
        sapi.grant_local_roles_for(patient, roles=["Owner"], user=TAMANU_ID)

        # don't allow the edition, but to tamanu (Owner) only
        sapi.manage_permission_for(patient, ModifyPortalContent, ["Owner"])

        # re-index object security indexes (e.g. allowedRolesAndUsers)
        patient.reindexObjectSecurity()

        # flush the object from memory
        patient._p_deactivate()


def sync_service_requests(session, since=15, dry_mode=True):
    # get the service requests created/modified since?
    since = timedelta(days=-since)
    resources = session.get_resources(
        "ServiceRequest", _lastUpdated=since
    )
    for sr in resources:

        # get the Tamanu's test ID for this ServiceRequest
        tid = sr.getLabTestID()

        # get the sample for this ServiceRequest, if any
        sample = sr.getObject()

        # skip if sample does not exist yet and no valid status
        if not sample and sr.status in SKIP_STATUSES:
            logger.info("Skip (%s): %s" % (sr.status, tid))
            continue

        # skip if sample is up-to-date
        tamanu_modified = tapi.get_tamanu_modified(sr)
        sample_modified = tapi.get_tamanu_modified(sample)
        if sample and tamanu_modified <= sample_modified:
            logger.info("Skip (up-to-date): %s %s" % (tid, repr(sample)))
            continue

        # skip if the sample cannot be edited
        if sample and api.get_review_status(sample) in SAMPLE_FINAL_STATUSES:
            logger.warn("Skip (non-active): %s %s" % (tid, repr(sample)))
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
        sample_point_uid = api.get_uid(sample_point) if sample_point else None

        # date sampled
        date_sampled = specimen.get_date_sampled()

        # get the priority
        priority = sr.get("priority")
        priority = dict(PRIORITIES).get(priority, "5")

        # get the remarks (notes)
        remarks = get_remarks(sr)

        # get or create the client via FHIR's encounter/serviceProvider
        client = get_client(sr)

        # get or create the contact via FHIR's requester
        contact = get_contact(sr)

        # get or create the patient via FHIR's subject
        patient_resource = sr.getPatientResource()
        patient = get_patient(patient_resource)
        patient_mrn = patient.getMRN()
        patient_dob = patient.getBirthdate()
        patient_sex = patient.getSex()
        patient_name = {
            "firstname": patient.getFirstname(),
            "middlename": patient.getMiddlename(),
            "lastname": patient.getLastname(),
        }

        # get profiles
        profiles = get_profiles(sr)
        profiles = map(api.get_uid, profiles)

        # get the services
        services = get_services(sr)

        # create the sample
        values = {
            "Client": client,
            "Contact": contact,
            "SampleType": sample_type,
            "SamplePoint": sample_point,
            "Site": sample_point_uid,
            "DateSampled": date_sampled,
            "Profiles": profiles,
            "MedicalRecordNumber": {"value": patient_mrn},
            "PatientFullName": patient_name,
            "DateOfBirth": patient_dob,
            "Sex": patient_sex,
            "Priority": priority,
            "ClientOrderNumber": tid,
            "Remarks": remarks,
            #"Ward": api.get_uid(ward),
            #"ClinicalInformation": "",
            #"DateOfAdmission": doa,
            #"CurrentAntibiotics": antibiotics,
            #"Volume": volume,
            # TODO WardDepartment: sr.get("encounter").get("location")?
            #"WardDepartment": department,
            #"Location": dict(LOCATIONS).get("location", ""),
        }
        request = api.get_request() or api.get_test_request()
        if sample:
            # edit sample
            edit_sample(sample, **values)
            logger.info("Object edited: %s %s" % (tid, repr(sample)))
        else:
            # create the sample
            sample = create_sample(client, request, values, services)
            logger.info("Object created: %s %s" % (tid, repr(sample)))

        # link the tamanu resource to this sample
        tapi.link_tamanu_resource(sample, sr)

        # do the transition
        action = dict(TRANSITIONS).get(sr.status)
        if action:
            doActionFor(sample, action)
            logger.info("Action (%s): %s %s" % (action, tid, repr(sample)))


def edit_sample(sample, **kwargs):
    # pop non-editable fields
    fields = api.get_fields(sample)
    for field_name, field in fields.items():
        # cannot update readonly fields
        readonly = getattr(field, "readonly", False)
        if readonly:
            kwargs.pop(field_name, None)

        # check field writable permission
        perm = getattr(field, "write_permission", ModifyPortalContent)
        if perm and not sapi.check_permission(perm, sample):
            kwargs.pop(field_name, None)

    # edit the sample
    api.edit(sample, **kwargs)


def error(message):
    """Exit with error
    """
    print("ERROR: %s" % message)
    exit(1)


def main(app):
    args, _ = parser.parse_known_args()
    if hasattr(args, "help") and args.help:
        print("")
        parser.print_help()
        parser.exit()
        return

    # get the remote host
    host = args.tamanu_host
    if not host:
        error("Remote URL is missing")

    # get the user and password
    try:
        user, password = args.tamanu_user.split(":")
    except (AttributeError, ValueError):
        error("Credentials are missing or not valid format")
        return

    # get since days
    since = api.to_int(args.since, default=5)

    # dry mode
    trues = ["True", "true", "1", "yes", "y"]
    dry = args.dry in trues

    # mapping of supported resource types and sync functions
    resources = {
        "Patient": sync_patients,
        "ServiceRequest": sync_service_requests
    }

    # get the resource type to synchronize
    sync_func = resources.get(args.resource)
    if not sync_func:
        error("Resource type is missing or not valid")

    # Setup environment
    setup_script_environment(app, stream_out=False)

    # Start a session with Tamanu server
    session = TamanuSession(host)
    logged = session.login(user, password)
    if not logged:
        error("Cannot login, wrong credentials")

    # Call the sync function
    sync_func(session, since=since, dry_mode=dry)

    if dry:
        # Dry mode. Do not do transaction
        print("Dry mode. No changes done")
        return

    # Commit transaction
    logger.info("Commit transaction ...")
    transaction.commit()
    logger.info("Commit transaction [DONE]")


if __name__ == "__main__":
    main(app)  # noqa: F821
