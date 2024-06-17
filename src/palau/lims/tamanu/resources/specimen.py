# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.core.catalog import SETUP_CATALOG
from palau.lims.tamanu.resources import TamanuResource

_marker = object()


class SpecimenResource(TamanuResource):

    def _get_object_by_title(self, portal_type, title):
        if not title:
            return None
        query = {
            "portal_type": portal_type,
            "title": title
        }
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            obj = api.get_object(brains[0])
            return obj

        # TODO QA Searches are case-aware, fallback to direct search by title
        del(query["title"])
        title = title.strip().lower()
        for brain in api.search(query, SETUP_CATALOG):
            name = api.get_title(brain).strip().lower()
            if name == title:
                return api.get_object(brain)

        return None

    def get_sample_type(self):
        """Get sample type from resource payload
        """
        # TODO Wrap all this in a SpecimenTypeResource.getObject()
        info = self.get_sample_type_info()
        title = info.get("title")
        # TODO QA We search by sample type title instead of prefix!
        return self._get_object_by_title("SampleType", title=title)

    def get_collection(self):
        return self.get("collection")

    def get_sample_point(self):
        """Get sample point from resource payload
        """
        # TODO Wrap all this in a SamplePointResource.getObject()
        info = self.get_sample_point_info()
        title = info.get("title")
        # TODO QA We search by sample point title instead of code!
        return self._get_object_by_title("SamplePoint", title=title)

    def get_date_sampled(self):
        collection = self.get_collection()
        return collection.get("collectedDateTime")

    def get_sample_type_info(self):
        """Returns a dict-like object that represents a SampleType based on the
        information provided in the current resource
        """
        specimen_type = self.get("type")
        if not specimen_type:
            raise ValueError("Specimen without type: %r" % self)
        coding = specimen_type.get("coding")
        if not coding:
            return {}
        return {
            "title": coding[0].get("display"),
            "Prefix": coding[0].get("code"),
        }

    def get_sample_point_info(self):
        """Returns a dict-like object that represents a SamplePoint based on
        the information provided in the current resource
        """
        collection = self.get_collection()
        body_site = collection.get("bodySite")
        if not body_site:
            return {}
        coding = body_site.get("coding")
        if not coding:
            return {}
        return {
            "title": coding[0].get("display"),
            "code": coding[0].get("code"),
        }
