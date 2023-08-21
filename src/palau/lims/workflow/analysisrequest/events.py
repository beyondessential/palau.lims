# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from palau.lims import utils


def after_verify(sample):
    """Event fired when a sample gets verified
    """
    # The text Insufficient volume of sample set for field "Not enough volume
    # text" (from either the Sample Type or Sample Template) is automatically
    # inserted in the "Results Interpretation" field (section "General") when
    # there is not enough volume
    # https://github.com/beyondessential/pnghealth.lims/issues/24
    if not utils.is_enough_volume(sample):
        field_name = "InsufficientVolumeText"

        # Rely first on the template
        template = sample.getTemplate()
        msg = template and utils.get_field_value(template, field_name) or ""

        if not msg:
            # Fallback to message from sample type
            samp_type = sample.getSampleType()
            msg = utils.get_field_value(samp_type, field_name)

        if msg:
            # Store the message in Results Interpretation (General)
            prev = sample.getResultsInterpretation()
            msg = "<br/>".join([msg, prev])
            sample.setResultsInterpretation(msg)
