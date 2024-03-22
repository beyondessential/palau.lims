# -*- coding: utf-8 -*-


from bika.lims import api
from palau.lims.tamanu import api as tapi
from plone.app.layout.viewlets import ViewletBase


class TamanuObjectViewlet(ViewletBase):

    def is_visible(self):
        metadata = self.get_tamanu_metadata()
        if not metadata:
            return False
        return True

    def get_tamanu_metadata(self):
        """Returns the metadata that represents the original resource the
        current context was built from on import, if any
        """
        if tapi.is_tamanu_content(self.context):
            return tapi.get_tamanu_storage(self.context)
        return None

    def get_tamanu_metadata_url(self):
        """Returns the url that displays the original resource the current
        context was built from on import, if any
        """
        return "{}/tamanu_metadata".format(api.get_url(self.context))
