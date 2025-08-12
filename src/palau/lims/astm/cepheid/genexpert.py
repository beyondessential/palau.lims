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

import collections

from bika.lims import api
from palau.lims.astm import ASTMBaseImporter as Base

# 4. test_id:             Chlamydia       Gonorrhea     HBV-VL
# 5. test_name:           Xpert CT_NG     Xpert CT_NG   Xpert HBV Viral Load
# 6. test_version:        3               3             1
# 7. analyte_name         CT              NG
# 8. complementary_name

KEYWORDS_MAPPING = (
    # Tuple of (instrument_parameter, (service_keywords))
    # R|1|^CTNG^^Chlamydia^Xpert CT_NG^3^CT^|NOT DETECTED^||
    ("Chlamydia", ["Chlamydia"]),
    ("CT", ["Chlamydia"]),
    # R|11|^CTNG^^Gonorrhea^Xpert CT_NG^3^NG^|NOT DETECTED^||
    ("Gonorrhea", ["Gonorrhea"]),
    ("NG", ["Gonorrhea"]),
    # R|1|^^^HBV-VL^Xpert HBV Viral Load^1^^|^22.21|IU/mL|
    ("HBV-VL", ["HBV-VL"]),
    # R|1|^^^HCV-VL^Xpert_HCV Viral Load^1^^|NOT DETECTED^|IU/mL|
    ("HCV-VL", ["HCV-VL"]),
    # R|1|^^^HIV-VL^Xpert_HIV-1 Viral Load^1^^|^47473.65|copies/mL|
    ("HIV-VL", ["HIV-VL"]),
    # R|1|^XpertRES^^XpertCov^Xpress SARS-CoV-2_Flu_RSV plus^1^SARS-CoV-2^|NEGATIVE^||
    ("XpertCov", ["XpertCov", "COVID-RT-PCR", "COVID-RDT"]),
    ("SARS-CoV-2", ["XpertCov", "COVID-RT-PCR", "COVID-RDT"]),
    # R|8|^XpertRES^^XpertFluA^Xpress SARS-CoV-2_Flu_RSV plus^1^Flu A^|NEGATIVE^||
    ("XpertFluA", ["XpertFluA"]),
    ("Flu A", ["XpertFluA"]),
    # R|18|^XpertRES^^XpertFluB^Xpress SARS-CoV-2_Flu_RSV plus^1^Flu B^|NEGATIVE^||
    ("XpertFluB", ["XpertFluB"]),
    ("Flu B", ["XpertFluB"]),
    # R|25|^XpertRES^^XpertRSV^Xpress SARS-CoV-2_Flu_RSV plus^1^RSV^|NEGATIVE^||
    ("XpertRSV", ["XpertRSV"]),
    ("RSV", ["XpertRSV"]),
    # R|1|^X-Carba^^IMP^Xpert_Carba-R^1^IMP^|NOT DETECTED^||
    ("IMP", []),
    # R|8|^X-Carba^^VIM^Xpert_Carba-R^1^VIM^|NOT DETECTED^||
    ("VIM", []),
    # R|15|^X-Carba^^NDM^Xpert_Carba-R^1^NDM^|NOT DETECTED^||
    ("NDM", []),
    # R|22|^X-Carba^^KPC^Xpert_Carba-R^1^KPC^|NOT DETECTED^||
    ("KPC", []),
    # R|29|^X-Carba^^OXA48^Xpert_Carba-R^1^OXA48^|NOT DETECTED^||
    ("OXA48", []),
)


class ASTMImporter(Base):
    """Results importer for Cepheid GeneXpert
    """

    @property
    def keywords_mapping(self):
        return dict(KEYWORDS_MAPPING)

    def get_sender(self):
        """Return the instrument name, serial and version

        :returns: Tuple of instrument name, serial, version
        """
        header = self.get_header()
        if not header:
            return None
        sender = header.get("sender", {})
        name = sender.get("name", "")
        serial = sender.get("id", "")
        version = sender.get("software_version", "")
        return name, serial, version

    def get_patient(self):
        """Returns the (P)atient record of this astm message
        """
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

        # Fallback to Patient ID 1
        pid = patient.get("id")
        if pid:
            return pid

        # Fallback to Patient ID 2 (Practice-assigned ID)
        pid = patient.get("practice_id")
        if pid:
            return pid

        return default

    def is_main_result(self, record):
        """Returns whether the result record is a main result
        """
        test = record.get("test")
        if not test:
            return False

        # must have both name and version
        name = test.get("test_name")
        version = test.get("test_version")
        if not all([name, version]):
            return False

        # and complementary name must be empty
        complementary = test.get("complementary_name")
        if complementary:
            return False

        return True

    def get_test_key(self, result):
        """Returns the test key used for grouping tests, that is made of the
        concatenation of the panel_id + test_id
        """
        test = result.get("test") or {}
        panel_id = test.get("panel_id") or ""
        test_id = test.get("test_id") or ""
        return ".".join([panel_id, test_id])

    def group_by_test(self, results):
        """Groups the ASTM results by test
        """
        groups = collections.OrderedDict()
        for result in results:
            key = self.get_test_key(result)
            groups.setdefault(key, []).append(result)
        return groups

    def to_interim(self, result):
        """Converts the result to an interim-compliant dict
        """
        test = result.get("test") or {}
        analyte_name = test.get("analyte_name")
        complementary_name = test.get("complementary_name")
        parts = list(filter(None, [analyte_name, complementary_name]))
        if not parts:
            return None

        result_value = self.get_test_result(result)
        result_type = "" if api.is_floatable(result) else "string"
        return {
            "keyword": "_".join(parts),
            "title": ".".join(parts),
            "value": result_value,
            "choices": [],
            "result_type": result_type,
            "allow_empty": True,
            "unit": self.get_test_units(result),
            "hidden": False,
            "wide": False,
        }

    def get_results(self):
        """Return the (R)esult records that are considered as main results
        """
        results = super(ASTMImporter, self).get_results()

        # extract main results
        main_results = [r for r in results if self.is_main_result(r)]

        # extract secondary (analyte and complementary) results
        sec_results = [r for r in results if r not in main_results]

        # group secondary results by test
        sec_by_test = self.group_by_test(sec_results)

        # assign secondary results to main result
        for result in main_results:

            # get the test full key
            key = self.get_test_key(result)

            # get the analyte and complementary results
            secondaries = sec_by_test.get(key)
            for secondary in secondaries:
                # convert to an interim-like record
                interim = self.to_interim(secondary)
                if not interim:
                    continue
                # add as an interim result field
                result.setdefault("interims", []).append(interim)

        # return the main results (with interims)
        return main_results

    def get_test_result(self, record):
        """Returns the qualitative or quantitative result of the result record
        """
        value = record.get("value") or {}
        qualitative = value.get("qualitative_result")
        if qualitative:
            return qualitative
        return value.get("quantitative_result") or ""

    def get_test_id(self, record):
        """Returns the test ID from the given results record
        """
        test = record.get("test") or {}

        # give priority to the analyte_name over test_id
        analyte_name = test.get("analyte_name")
        if analyte_name:
            return analyte_name

        # fall-back to test_id
        return test.get("test_id") or ""
