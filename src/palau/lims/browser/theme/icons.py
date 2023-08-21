# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import os

from plone.resource.interfaces import IResourceDirectory
from senaite.core.browser.globals.interfaces import IIconProvider
from senaite.core.browser.globals.interfaces import ISenaiteTheme
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implementer

ICON_BASE_URL = "++plone++palau.lims.static/assets/icons"


@implementer(IIconProvider)
class IconProvider(object):
    adapts(ISenaiteTheme)

    def __init__(self, view, context):
        self.view = view
        self.context = context

    def icons(self):
        icons = {}
        static_dir = getUtility(
            IResourceDirectory, name=u"++plone++palau.lims.static")
        icon_dir = static_dir["assets"]["icons"]
        for icon in icon_dir.listDirectory():
            name, ext = os.path.splitext(icon)
            icons[name] = "{}/{}".format(ICON_BASE_URL, icon)
            icons[icon] = "{}/{}".format(ICON_BASE_URL, icon)
        return icons
