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


from AccessControl import ClassSecurityInfo
from palau.lims import messageFactory as _
from palau.lims.behaviors import get_behavior_schema
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFCore import permissions
from senaite.core.schema import UIDReferenceField
from senaite.core.z3cform.widgets.uidreference import UIDReferenceWidget
from senaite.patient.config import PATIENT_CATALOG
from senaite.patient.interfaces import IPatient
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IExtendedPatientBehavior(model.Schema):

    replaced_by = UIDReferenceField(
        title=_(u"Replaced By Patient"),
        allowed_types=("Patient", ),
        multi_valued=False,
        required=False,
    )

    directives.widget(
        "replaced_by",
        UIDReferenceWidget,
        query={
            "portal_type": "Patient",
            "is_active": True,
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        },
        display_template="<a href='${url}'>${firstname} ${middlename} ${"
                         "lastname}</a>",
        columns=[
            {
                "name": "title",
                "label": _(u"Title"),
            }
        ],
        catalog=PATIENT_CATALOG
    )


@implementer(IExtendedPatientBehavior)
@adapter(IPatient)
class ExtendedPatient(object):

    security = ClassSecurityInfo()

    def __init__(self, context):
        self.context = context
        self._schema = None

    @property
    def schema(self):
        """Return the schema provided by the underlying behavior
        """
        if self._schema is None:
            behavior = IExtendedPatientBehavior
            behavior_schema = get_behavior_schema(self.context, behavior)
            if not behavior_schema:
                raise TypeError("Not a valid context")
            self._schema = behavior_schema
        return self._schema

    @security.private
    def accessor(self, fieldname):
        """Return the field accessor for the fieldname
        """
        if fieldname not in self.schema:
            return None
        return self.schema[fieldname].get

    @security.private
    def mutator(self, fieldname):
        """Return the field mutator for the fieldname
        """
        if fieldname not in self.schema:
            return None
        return self.schema[fieldname].set

    @security.protected(permissions.ModifyPortalContent)
    def setReplacedBy(self, value):     # noqa CamelCase
        """Setter for the replaced_by field
        """
        mutator = self.mutator("replaced_by")
        return mutator(self, value)

    @security.protected(permissions.View)
    def getReplacedBy(self):     # noqa CamelCase
        """Getter for the replaced_by field
        """
        accessor = self.accessor("replaced_by")
        return accessor(self)

    replaced_by = property(getReplacedBy, setReplacedBy)
