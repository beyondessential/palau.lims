# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims import api


def get_rejection_pdf(sample):
    """Generates a pdf with sample rejection reasons
    """
    # Avoid circular dependencies
    from palau.lims.browser.sample.rejection import RejectionPdfView

    # Generate the pdf document
    view = RejectionPdfView(sample, api.get_request())
    return view.create_pdf()
