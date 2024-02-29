# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims.interfaces.analysis import IRequestAnalysis
from plone.indexer import indexer


@indexer(IRequestAnalysis)
def date_sampled(instance):
    """Returns the date when the sample the analysis belongs to was collected
    """
    sample = instance.getRequest()
    return sample.getDateSampled()
