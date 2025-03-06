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

from palau.lims.adapters.stickers import StickerTemplates


def get_sample_stickers(self, request):
    """Returns an array with the templates of stickers available for Sample
    object in context.
    Each array item is a dictionary with the following structure:
        [{'id': <template_id>,
         'title': <teamplate_title>,
         'selected: True/False'}, ]
    """

    sample_type = self.context.getSampleType()
    sticker_ids = sample_type.getAdmittedStickers()
    if request.get("size", "") == "small":
        default_sticker_id = sample_type.getDefaultSmallSticker()
    else:
        default_sticker_id = sample_type.getDefaultLargeSticker()

    available_templates = []
    product_templates = StickerTemplates(self.context).get_product_templates()
    for template in product_templates:
        template_id = template.get("id")
        template.update({
            "selected": default_sticker_id == template_id
        })
        if template_id in sticker_ids:
            available_templates.append(template)

    if not available_templates:
        # Sample Type does not have addmitted templates set or are not from
        # this product. Return all templates
        available_templates = product_templates

    return available_templates
