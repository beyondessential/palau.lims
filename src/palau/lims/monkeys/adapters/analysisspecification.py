# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd
from bika.lims import api
from bika.lims.utils import format_supsub
from bika.lims.utils import get_image
from bika.lims.utils import get_link
from bika.lims.config import MAX_OPERATORS
from bika.lims.config import MIN_OPERATORS


def folderitem(self, obj, item, index):
    """Service triggered each time an item is iterated in folderitems.

    The use of this service prevents the extra-loops in child objects.

    :obj: the instance of the class to be foldered
    :item: dict containing the properties of the object to be used by
        the template
    :index: current index of the item
    """
    # ensure we have an object and not a brain
    obj = api.get_object(obj)
    url = api.get_url(obj)
    title = api.get_title(obj)
    keyword = obj.getKeyword()
    unit = obj.getUnit()

    # Unit
    item["Unit"] = unit and format_supsub(unit) or ""

    # dynamic analysisspecs
    dspecs = self.get_dynamic_analysisspecs()
    dspec = dspecs.get(keyword)
    # show the dynamic specification icon next to the Keyword
    if dspec:
        item["before"]["Keyword"] = get_image(
            "dynamic_analysisspec.png",
            title=_("Found Dynamic Analysis Specification for '{}' in '{}'"
                    .format(keyword, self.dynamic_spec.Title())))

    # get the category
    if self.show_categories_enabled():
        category = obj.getCategoryTitle()
        if category not in self.categories:
            self.categories.append(category)
        item["category"] = category

    item["Title"] = title
    item["replace"]["Title"] = get_link(url, value=title)
    item["choices"]["min_operator"] = self.min_operator_choices
    item["choices"]["max_operator"] = self.max_operator_choices
    item["allow_edit"] = self.get_editable_columns()
    item["required"] = self.get_required_columns()

    spec = self.specification.get(keyword, {})

    item["selected"] = spec and True or False
    item["min"] = spec.get("min", "")
    item["max"] = spec.get("max", "")
    item["warn_min"] = spec.get("warn_min", "")
    item["warn_max"] = spec.get("warn_max", "")
    item["hidemin"] = spec.get("hidemin", "")
    item["hidemax"] = spec.get("hidemax", "")
    item["rangecomment"] = spec.get("rangecomment", "")

    # min/max operators
    max_op = spec.get("max_operator", "leq")
    min_op = spec.get("min_operator", "geq")
    if self.allow_edit:
        item["max_operator"] = max_op
        item["min_operator"] = min_op
    else:
        # Render display values instead of the raw values
        item["max_operator"] = MAX_OPERATORS.getValue(max_op)
        item["min_operator"] = MIN_OPERATORS.getValue(min_op)

    # Add methods
    methods = obj.getMethods()
    if methods:
        links = map(
            lambda m: get_link(
                m.absolute_url(), value=m.Title(), css_class="link"),
            methods)
        item["replace"]["Methods"] = ", ".join(links)
    else:
        item["methods"] = ""

    # Icons
    after_icons = ""
    if obj.getAccredited():
        after_icons += get_image(
            "accredited.png", title=_("Accredited"))
    if obj.getAttachmentRequired():
        after_icons += get_image(
            "attach_reqd.png", title=_("Attachment required"))
    if after_icons:
        item["after"]["Title"] = after_icons

    return item
