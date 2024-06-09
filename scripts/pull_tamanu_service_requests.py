# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

import argparse
import requests
from pull_tamanu_patients import basic_auth

# the id of the consumer for analysis request creation and update
SERVICE_REQUEST_CONSUMER = "tamanu.consumers.analysisrequest"
CATEGORY_URL = "http://snomed.info/sct|108252007"

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


def pull_tamanu_service_requests(args):
    """
    Send a PULL request against ServiceRequest endpoint and response patients
    """
    # Login to get access token from Tamanu
    token = get_tamanu_token(args)
    headers = {"Authorization": "Bearer {}".format(token)}

    # Send GET request to Tamanu /Patients endpoint to fetch data
    service_request_endpoint = (
        "{}/v1/integration/fhir/mat/ServiceRequest".format(
            args.tamanu_domain)
    )
    params = {
        "_lastUpdated": "gt{}".format(args.last_updated),
        "category": CATEGORY_URL,
    }

    service_request_response = requests.get(
        service_request_endpoint,
        params=params,
        headers=headers
    )
    service_requests = service_request_response.json().get("entry", [])

    return service_requests


def push_tamanu_service_requests(args, service_requests):
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
        "consumer": SERVICE_REQUEST_CONSUMER,
        "service_requests": service_requests
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
    parser.add_argument("--senaite_domain", "-sd", help="Senaite Domain")
    parser.add_argument("--senaite_username", "-su", help="Senaite Username")
    parser.add_argument("--senaite_password", "-sp", help="Senaite Password")

    args = parser.parse_args()
    service_requests = pull_tamanu_service_requests(args)
    push_tamanu_service_requests(args, service_requests)


if __name__ == "__main__":
    main()
