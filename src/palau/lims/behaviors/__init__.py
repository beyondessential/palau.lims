# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from plone.dexterity.utils import getAdditionalSchemata


def get_behavior_schema(context, behavior):
    """Returns the schema of the context that is provided by the behavior
    interface passed-in, if any
    """
    schemata = getAdditionalSchemata(context=context)
    for sch in schemata:
        if sch.isOrExtends(behavior):
            return sch
    return None
