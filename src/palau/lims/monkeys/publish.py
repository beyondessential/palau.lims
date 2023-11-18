# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from slugify import slugify


def get_report_filename(self, report):
    """Generate the filename for the sample PDF
    sample ID_MRN_pt name_ward

    e.g. PB22A012_TA000314_Minnie Mouse_ED
    :return:
    """
    sample = report.getAnalysisRequest()
    ward = sample.getWard()
    parts = [
        api.get_id(sample),
        sample.getMedicalRecordNumberValue() or "",
        sample.getPatientFullName() or "",
        api.get_title(ward) if ward else "",
        ]
    parts = [slugify(prt, separator="-", lowercase=False) for prt in parts]
    filename = "_".join(parts)
    return "{}.pdf".format(filename)
