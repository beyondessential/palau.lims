# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.core.catalog import SETUP_CATALOG
from palau.lims.tamanu.resources import TamanuResource

_marker = object()

class SpecimenResource(TamanuResource):

    def get_sample_type(self):
        """Get sample type from resource payload
        """
        specimen_type = self.get("type")
        coding = specimen_type.get("coding")
        query = {
            "portal_type": "SampleType",
            "is_active": True,
            "title": coding[0].get("code"),
        }
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            sample_type = api.get_object(brains[0])
            return sample_type
        return None

    def get_collection(self):
        return self.get("collection")

    def get_site(self):
        collection = self.get_collection()
        body_site = collection.get("bodySite")
        coding = body_site.get("coding")
        query = {
            "portal_type": "SamplePoint",
            "is_active": True,
            "title": coding[0].get("code"),
        }
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            site = api.get_object(brains[0])
            return site
        return None

    def get_date_sampled(self):
        collection = self.get_collection()
        return collection.get("collectedDateTime")
