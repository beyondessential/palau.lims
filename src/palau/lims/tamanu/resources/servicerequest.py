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
