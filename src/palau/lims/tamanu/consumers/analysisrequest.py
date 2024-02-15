# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd


from bika.lims import api
from bika.lims.utils.analysisrequest import create_analysisrequest
from DateTime import DateTime
from senaite.core.catalog import SAMPLE_CATALOG
from senaite.jsonapi.interfaces import IPushConsumer
from zope import interface


class AnalysisRequestPushConsumer(object):
    """Adapter that handles push requests for AnalysisRequest
    """
    interface.implements(IPushConsumer)

    def __init__(self, data):
        self.data = data

    def process(self):
        """Creates objects from ServiceRequest type based on the data provided
        """
        service_requests = self.get_service_requests_data(self.data)
        for service_request in service_requests:
            self.create_service_request(service_request)
        return True

    def get_service_requests_data(self, data):
        """Get list of service_requests from payload
        """
        return data.get("service_requests", [])

    def get_service_request_info(self, service_request_resource):
        """Convert to service request dict from service request object data
        """
        date_now = DateTime().strftime("%Y-%m-%d")
        client_uid = self.get_uid(service_request_resource["encounter"])
        contact_uid = self.get_uid(service_request_resource["requester"])

        return {
            "Client": client_uid,
            "Contact": contact_uid,
            "DateSampled": date_now
        }

    def exists(self, id):
        cat = api.get_tool(SAMPLE_CATALOG)
        brains = cat(getId=id)
        return len(brains) > 0

    def get_uid(self, obj):
        """Get, split and return uid from reference
        """
        reference = obj["reference"]
        parts = reference.split("/")
        value = parts[1].encode()
        uid = value.replace('-', '')
        return uid

    def get_client(self, service_request_client):
        """Get Client object
        """
        client_uid = self.get_uid(service_request_client)
        client = api.get_object(client_uid)
        return client

    def create_service_request(self, service_request_data):
        service_request_resource = service_request_data["resource"]
        record = self.get_service_request_info(service_request_resource)

        if not self.exists(service_request_resource["id"]):
            client = self.get_client(service_request_resource["encounter"])

            create_analysisrequest(client, {}, record)
        else:
            # Update analysis request
            pass
