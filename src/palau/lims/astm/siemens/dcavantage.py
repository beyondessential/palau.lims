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

from palau.lims.astm import ASTMBaseImporter as Base


KEYWORDS_MAPPING = (
    # Tuple of (instrument_parameter, (service_keywords))
    ("Crt", ["creat", "CREAT_A", "UCREA", "CREAT_V"]),
    ("Alb", ["Alb", "UALB"]),
    ("Ratio", ["MALB"]),
    ("HbA1c", ["HbA1c"]),
)


class ASTMImporter(Base):
    """Results importer for SIEMENS DCA Vantage Analyzer
    """

    @property
    def keywords_mapping(self):
        return dict(KEYWORDS_MAPPING)

    def get_patient(self):
        patients = self.get_patients()
        if len(patients) != 1:
            return {}
        return patients[0]

    def get_sample_id(self, default=None):
        """Get the Sample ID
        """
        sample_id = super(ASTMImporter, self).get_sample_id(default=default)
        if sample_id:
            return sample_id

        # Fallback to patient record's practice_id
        patient = self.get_patient()
        if not patient:
            return default

        sid = patient.get("practice_id")
        if not sid:
            return default

        return sid

    def get_test_id(self, record):
        """Returns the test ID from the given results record
        """
        test = record.get("test") or {}
        param = test.get("parameter") or ""
        return param.strip()

    def get_captured_date(self, record):
        """Returns the date when the result was captured
        """
        return record.get("started_at")
