# -*- coding: utf-8 -*-

from palau.lims.tamanu.resources import TamanuResource


class ServiceRequest(TamanuResource):
    """Object that represents a ServiceRequest resource from Tamanu
    """

    def getPatientResource(self):
        """Returns the Patient resource assigned to this ServiceRequest, if any
        """
        return self.get("subject")

    def getSpecimenResource(self):
        """Returns the SampleType resource assigned to this ServiceRequest
        """
        specimen = self.get("specimen")
        return map(self.get_reference, specimen)

    def getEncounter(self):
        """Returns the Encounter resource assigned to this ServiceRequest
        """
        return self.get("encounter")

    def getServiceProvider(self):
        """Returns the Organization that provides the service
        """
        encounter = self.getEncounter()
        if not encounter:
            return None
        return encounter.getServiceProvider()

    def getRequester(self):
        """Returns the Requester resource (Practitioner)
        """
        return self.get("requester")
