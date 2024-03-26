# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.core.catalog import SETUP_CATALOG
from palau.lims.tamanu.resources import TamanuResource

_marker = object()


class SpecimenResource(TamanuResource):

    def get_sample_type(self):
        """Get sample type from resource payload
        """
        # TODO Wrap all this in a SpecimenTypeResource.getObject()
        info = self.get_sample_type_info()
        title = info.get("title")
        if not title:
            return None

        # TODO QA We search by sample type title instead of prefix!
        query = {
            "portal_type": "SampleType",
            "is_active": True,
            "title": title,
        }
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            sample_type = api.get_object(brains[0])
            return sample_type

        # TODO QA Searches are case-aware, fallback to direct search by title
        del(query["title"])
        title = title.strip().lower()
        for brain in api.search(query, SETUP_CATALOG):
            name = api.get_title(brain).strip().lower()
            if name == title:
                return api.get_object(brain)

        return None

    def get_collection(self):
        return self.get("collection")

    def get_site(self):
        collection = self.get_collection()
        body_site = collection.get("bodySite")
        if not body_site:
            return None
        coding = body_site.get("coding")
        if not coding:
            return None

        # TODO QA We search by sample point name instead of code!
        #term = coding[0].get("code")
        term = coding[0].get("display")
        if not term:
            return None

        query = {
            "portal_type": "SamplePoint",
            "is_active": True,
            "title": term,
        }
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            return api.get_object(brains[0])

        # TODO QA Searches are case-aware, fallback to direct search by title
        del(query["title"])
        term = term.strip().lower()
        for brain in api.search(query, SETUP_CATALOG):
            title = api.get_title(brain).strip().lower()
            if title == term:
                return api.get_object(brain)

        return None

    def get_date_sampled(self):
        collection = self.get_collection()
        return collection.get("collectedDateTime")

    def get_sample_type_info(self):
        """Returns a dict-like object that represents a SampleType based on the
        information provided in the current resource
        """
        specimen_type = self.get("type")
        coding = specimen_type.get("coding")
        if not coding:
            return {}
        return {
            "title": coding[0].get("display"),
            "Prefix": coding[0].get("code"),
        }
