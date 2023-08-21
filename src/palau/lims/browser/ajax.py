# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import six
from bika.lims import api
from bika.lims.decorators import returns_json
from palau.lims.utils import get_field_value
from Products.Five.browser import BrowserView
from senaite.core.api import measure as mapi
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.decorators import readonly_transaction


class Bottles(BrowserView):
    """Returns a JSON with the Container from Bottle-like types that are
    registered in the system
    """

    @readonly_transaction
    @returns_json
    def __call__(self):
        base_query = {
            "portal_type": "SampleContainer",
            "is_active": self.request.get("is_active", True),
            "sort_order": self.request.get("sord", "ascending"),
            "sort_on": self.request.get("sidx", "sortable_title"),
            "listing_searchable_text": self.request.get("SearchTerm"),
        }

        def has_value(item):
            item_value = item[1]
            if isinstance(item_value, six.string_types):
                item_value = item_value.strip()
            if item_value in [True, False, 0]:
                return True
            elif not item_value:
                return False
            return True

        def is_bactec_bottle(container):
            """Returns whether the container passed-in belongs to a content type
            with the setting BACTECBottle set to True
            """
            c_type = container.getContainerType()
            return get_field_value(c_type, "BACTECBottle", default=False)

        # Remove those keys with a non-valid value
        query = dict(filter(has_value, base_query.items()))
        objects = map(api.get_object, api.search(query, SETUP_CATALOG))

        # Skip those that are not BACTEC bottles
        objects = filter(is_bactec_bottle, objects)
        records = filter(None, map(self.get_item_info, objects))

        # Calculate pagination
        num_records = len(records)
        page_num = api.to_int(self.request.get("page"), 1)
        page_rows = api.to_int(self.request.get("rows"), 10)
        pages = num_records / page_rows
        pages += divmod(num_records, page_rows)[1] and 1 or 0

        # Subset of the records
        rows = records[(page_num - 1) * num_records: page_num * page_rows]
        return {
            "page": page_num,
            "total": pages,
            "records": num_records,
            "rows": rows
        }

    def get_item_info(self, obj):
        weight = get_field_value(obj, "weight") or 0
        if mapi.is_weight(weight):
            weight = mapi.get_quantity(weight, "g")

        return {
            "UID": api.get_uid(obj),
            "container_uid": api.get_uid(obj),
            "Container": api.get_title(obj),
            "Description": api.get_description(obj),
            "DryWeight": weight,
        }
