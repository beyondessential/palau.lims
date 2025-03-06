# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS.
#
# PALAU.LIMS is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2023-2025 by it's authors.
# Some rights reserved, see README and LICENSE.

from palau.lims import PRODUCT_NAME
from zope.interface import implementer
from bika.lims.vocabularies import getStickerTemplates
from bika.lims.interfaces import IGetStickerTemplates


@implementer(IGetStickerTemplates)
class StickerTemplates(object):
    """Adapter that returns the stickers available, that are only those
    registered in this add-on
    """

    def __init__(self, context):
        self.context = context

    def __call__(self, request):
        """Returns the templates from this add-on only
        """
        return self.get_product_templates()

    def get_product_templates(self):
        """Returns the templates from this add-on only
        """
        def is_from_product(template):
            template_id = template.get("id")
            return template_id.startswith(PRODUCT_NAME)

        templates = getStickerTemplates()
        templates = filter(is_from_product, templates)
        for template in templates:
            template.update({"selected": False})
        return templates
