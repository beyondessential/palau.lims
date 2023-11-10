# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

import argparse
import requests
from base64 import b64encode

# the id of the consumer for patients creation and update
PATIENT_CONSUMER = "tamanu.consumers.patient"


def get_tamanu_token(args):
    """
    Retrieve the tamanu token for other APIs
    """
    login_endpoint = "{}/v1/login".format(args.tamanu_domain)
    login_payload = {
        "email": args.tamanu_email,
        "password": args.tamanu_password
    }
    response = requests.post(login_endpoint, data=login_payload)
    return response.json().get("token")


def pull_tamanu_patients(args):
    """
    Send a PULL request against ServiceRequest endpoint and response patients
    """
    # Login to get access token from Tamanu
    token = get_tamanu_token(args)
    headers = {"Authorization": "Bearer {}".format(token)}

    # Send GET request to Tamanu /Patients endpoint to fetch data
    patient_endpoint = (
        "{}/v1/integration/fhir/mat/Patient".format(
            args.tamanu_domain)
    )
    params = {
        "_lastUpdated": "gt{}".format(args.last_updated),
        "active": "true",
        "_page": args.page,
        "_count": args.page_size
    }

    patient_response = requests.get(
        patient_endpoint,
        params=params,
        headers=headers
    )
    patients = patient_response.json().get("entry")

    return patients


def basic_auth(username, password):
    token = b64encode("{}:{}".format(username, password))
    return "Basic {}".format(token)


def push_tamanu_patients(args, patients):
    """
    Send patients payload to SENAITE
    """
    # Send PUSH request to SENAITE to update patients
    push_endpoint = (
        "{}/senaite/@@API/senaite/v1/push".format(
            args.senaite_domain)
    )
    token = basic_auth(args.senaite_username, args.senaite_password)
    headers = {"Authorization": "{}".format(token)}

    data = {
        "consumer": PATIENT_CONSUMER,
        "patients": patients
    }

    response = requests.post(
        push_endpoint,
        json=data,
        headers=headers,
    )
    response.raise_for_status()


def main():
    # Parse options
    parser = argparse.ArgumentParser(
        description="Script to update Patient to Senaite from Tamanu's payload"
    )
    parser.add_argument("--tamanu-domain", "-td", help="Tamanu domain")
    parser.add_argument("--tamanu-email", "-te", help="Tamanu email")
    parser.add_argument("--tamanu-password", "-tp", help="Tamanu password")
    parser.add_argument("--last_updated", "-lu", help="Last Updated")
    parser.add_argument("--page", "-p", help="Page", default=0)
    parser.add_argument("--page_size", "-ps", help="Page Size", default=20)
    parser.add_argument("--senaite_domain", "-sd", help="Senaite Domain")
    parser.add_argument("--senaite_username", "-su", help="Senaite Username")
    parser.add_argument("--senaite_password", "-sp", help="Senaite Password")

    args = parser.parse_args()
    patients = pull_tamanu_patients(args)
    push_tamanu_patients(args, patients)


if __name__ == "__main__":
    main()
