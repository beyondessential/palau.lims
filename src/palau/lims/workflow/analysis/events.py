# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims.interfaces import ISubmitted
from bika.lims.interfaces import IVerified
from bika.lims.workflow import doActionFor
from palau.lims.reflex import handle_reflex_testing
from zope.interface import alsoProvides


def after_submit(analysis):
    """Event fired when an analysis result gets submitted
    """
    # Handle reflex testing if necessary
    handle_reflex_testing(analysis, "submit")


def after_verify(analysis):
    """Event fired when an analysis result gets submitted
    """
    # Handle reflex testing if necessary
    handle_reflex_testing(analysis, "verify")


def after_set_out_of_stock(analysis):
    """Event fired when an analysis is transitioned to out-of-stock
    """
    # Mark the analysis with ISubmitted so samples with only one analysis in
    # out-of-stock can also be pre-published
    alsoProvides(analysis, ISubmitted)

    # Mark the analysis with IVerified so samples with only one analysis in
    # out-of-stock can also be published
    alsoProvides(analysis, IVerified)

    # Try to submit the sample
    sample = analysis.getRequest()
    doActionFor(sample, "submit")
