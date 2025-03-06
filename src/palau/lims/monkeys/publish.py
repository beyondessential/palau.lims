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
