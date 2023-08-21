# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

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
