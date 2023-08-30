# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from bika.lims.interfaces import ILabContact
from palau.lims import messageFactory as _
from palau.lims.content.fields import ExtBooleanField
from palau.lims.content.fields import ExtUIDReferenceField
from palau.lims.interfaces import IPalauLimsLayer
from Products.Archetypes.Widget import BooleanWidget
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import View
from senaite.core.browser.widgets import ReferenceWidget
from senaite.core.catalog import CLIENT_CATALOG
from zope.component import adapter
from zope.interface import implementer

# New fields to be added to this type
NEW_FIELDS = [
    ExtUIDReferenceField(
        "DefaultClient",
        allowed_types=("Client", ),
        required=False,
        multiValued=False,
        read_permission=View,
        write_permission=ModifyPortalContent,
        widget=ReferenceWidget(
            label=_(u"Default Hospital/Clinic"),
            description=_(
                u"The hospital or clinic to be selected by default on sample "
                u"creation"
            ),
            catalog_name=CLIENT_CATALOG,
            base_query={
                "is_active": True,
                "sort_on": "sortable_title",
                "sort_order": "ascending",
            },
            showOn=True,
        )
    ),
    ExtBooleanField(
        "AuthorisedRejection",
        default=False,
        widget=BooleanWidget(
            label=_("Can reject samples"),
            description=_(
                "Whether the user linked to this laboratory contact is "
                "authorised to reject samples. Note that user won't be able "
                "to reject a sample if she/he does not belong to an "
                "authorised group (LabManager or LabClerk), even if this "
                "option is selected"
            )
        )
    )
]


@adapter(ILabContact)
@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class LabContactSchemaExtender(object):
    """Extends Laboratory Contact type (LabContact) with additional fields
    """
    layer = IPalauLimsLayer

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return NEW_FIELDS
