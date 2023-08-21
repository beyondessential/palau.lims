# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from plone.dexterity.content import Container
from plone.supermodel import model

from senaite.core.interfaces import IHideActionsMenu

from zope.interface import implementer


class IWards(model.Schema):
    """Wards folder interface
    """
    # Implements IBasic behavior (title + description)
    pass


@implementer(IWards, IHideActionsMenu)
class Wards(Container):
    """Wards folder
    """
    pass
