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
        if not coding:
            return None

        # TODO QA We search by sample type title name of code!
        title = coding[0].get("display")
        prefix = coding[0].get("code")
        if not title:
            return None

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

        # TODO Create the Sample Type if not found?
        container = api.get_setup().bika_sampletypes
        return api.create(container, "SampleType", title=title, Prefix=prefix)

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
