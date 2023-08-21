# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd


from senaite.core.content.base import Container
from plone.supermodel import model

from senaite.core.interfaces import IHideActionsMenu

from zope.interface import implementer


class IWardDepartments(model.Schema):
    """Ward Departments folder interface
    """
    # Implements IBasic behavior (title + description)
    pass


@implementer(IWardDepartments, IHideActionsMenu)
class WardDepartments(Container):
    """Ward Departments folder
    """
    pass
