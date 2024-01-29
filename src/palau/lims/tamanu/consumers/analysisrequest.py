# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd


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


    def get_service_requests_data(self, data):
        """Get list of service_requests from payload
        """
        return data.get("service_requests", [])

    def get_service_request_info(self, service_request_resource):
        """Convert to service request dict from service request object data
        """
        pass


    def create_service_request(self, service_request_data):
        service_request_resource = service_request_data['resource']
        pass
