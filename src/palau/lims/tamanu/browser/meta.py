# -*- coding: utf-8 -*-

import json
from palau.lims.tamanu import api as tapi
from Products.Five.browser import BrowserView


class MetaView(BrowserView):

    def __call__(self):
        if tapi.is_tamanu_content(self.context):
            meta = tapi.get_tamanu_storage(self.context)
            return json.dumps(dict(meta))
        return "No metadata"
