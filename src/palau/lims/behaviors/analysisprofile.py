# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023-2024 Beyond Essential Systems Pty Ltd

from AccessControl import ClassSecurityInfo
from palau.lims import messageFactory as _
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.interfaces import IBehavior
from plone.supermodel import model
from Products.CMFCore import permissions
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.interfaces import IAnalysisProfile
from senaite.core.schema import UIDReferenceField
from senaite.core.z3cform.widgets.uidreference import UIDReferenceWidgetFactory
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IPalauAnalysisProfileBehavior(model.Schema):

    sample_types = UIDReferenceField(
        title=_(
            "label_analysisprofile_sampletypes",
            default="Sample types"
        ),
        description=_(
            "description_analysisprofile_sampletypes",
            default="Sample types for which this analysis profile is"
                    "supported."
        ),
        allowed_types=("SampleType", ),
        multi_valued=True,
        required=False,
    )

    directives.widget(
        "sample_types",
        UIDReferenceWidgetFactory,
        catalog=SETUP_CATALOG,
        query={
            "is_active": True,
            "sort_on": "title",
            "sort_order": "ascending",
        },
    )


@implementer(IBehavior, IPalauAnalysisProfileBehavior)
@adapter(IAnalysisProfile)
class PalauAnalysisProfileBehavior(object):

    security = ClassSecurityInfo()

    def __init__(self, context):
        self.context = context
        self._schema = None

    @security.protected(permissions.View)
    def getRawSampleTypes(self):
        accessor = self.context.accessor("sample_types", raw=True)
        return accessor(self.context) or []

    @security.protected(permissions.View)
    def getSampleTypes(self):
        accessor = self.context.accessor("sample_types")
        return accessor(self.context) or []

    @security.protected(permissions.ModifyPortalContent)
    def setSampleTypes(self, value):
        mutator = self.context.mutator("sample_types")
        mutator(self.context, value)
