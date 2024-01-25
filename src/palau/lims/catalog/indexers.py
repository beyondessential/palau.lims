# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from bika.lims.interfaces import IAnalysis
from bika.lims.interfaces import IAnalysisProfile
from bika.lims.interfaces.analysis import IRequestAnalysis
from plone.indexer import indexer
from senaite.core.catalog.indexer.senaitesetup import to_keywords_list


@indexer(IRequestAnalysis)
def date_sampled(instance):
    """Returns the date when the sample the analysis belongs to was collected
    """
    sample = instance.getRequest()
    return sample.getDateSampled()


@indexer(IAnalysisProfile)
def sampletype_title(instance):
    """Returns a list of titles from SampleType the instance is assigned to

    If the instance has no sample type assigned, it returns a tuple with
    a None value. This allows searches for `MissingValue` entries too.
    """
    sample_type = instance.getSampleTypes()
    return to_keywords_list(sample_type, api.get_title)


@indexer(IAnalysisProfile)
def sampletype_uid(instance):
    """Returns a list of uids from SampleType the instance is assigned to

    If the instance has no SampleType assigned, it returns a tuple with a None
    value. This allows searches for
    `MissingValue` entries too.
    """
    return instance.getRawSampleTypes() or [None]


@indexer(IAnalysis)
def department_title(instance):
    """Returns the title Department the instance is assigned to

    If the instance has no sample type assigned, it returns a tuple with
    a None value. This allows searches for `MissingValue` entries too.
    """
    sample_type = instance.getSampleTypes()
    return to_keywords_list(sample_type, api.get_title)