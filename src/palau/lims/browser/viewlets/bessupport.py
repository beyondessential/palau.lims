# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023-2024 Beyond Essential Systems Pty Ltd

from plone import api as ploneapi
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class BESSupportViewlet(ViewletBase):
    """Renders the script that displays the Zendesk's icon at bottom-left
    """
    index = ViewPageTemplateFile("templates/bessupport.pt")

    def is_visible(self):
        """Returns whether the viewlet is visible or not
        """
        if self.request.get("SERVER_NAME") == "localhost":
            return False
        return not ploneapi.user.is_anonymous()
