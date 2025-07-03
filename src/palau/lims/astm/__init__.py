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

import copy

from bika.lims import api
from bika.lims.workflow import doActionFor
from plone.memoize.instance import memoize
from senaite.core.api import dtime
from senaite.core.astm.importer import ASTMImporter as Base

ALLOWED_SAMPLE_STATES = ["sample_received"]

ALLOWED_ANALYSIS_STATES = ["unassigned", "assigned"]

DL_OPERANDS = ["<", ">"]


class ASTMBaseImporter(Base):
    """Basic ASTM results importer
    """

    def get_sender(self):
        """Return the instrument name, serial and version

        :returns: Tuple of instrument name, serial, version
        """
        name, serial, version = super(ASTMBaseImporter, self).get_sender()
        return name.strip(), serial.strip(), version.strip()

    @property
    @memoize
    def analyses_by_keyword(self):
        """Gets the analyses of the sample that are suitable for results input,
        grouped by keyword. Note that for a single keyword, more than one
        analysis can exist. Thus, a list for each keyword is returned
        """
        if not self.sample:
            return {}

        by_keyword = {}
        brains = self.sample.getAnalyses(review_state=ALLOWED_ANALYSIS_STATES)
        for brain in brains:
            obj = api.get_object(brain)
            keyword = obj.getKeyword()
            by_keyword.setdefault(keyword, []).append(obj)
        return by_keyword

    @property
    def keywords_mapping(self):
        return dict()

    def import_data(self):
        """Import data
        """
        if not self.instrument:
            return self.log("Cannot import results, instrument not found")

        if not self.sample:
            return self.log("Cannot import results, sample not found")

        # check sample status is valid
        state = api.get_review_status(self.sample)
        if state not in ALLOWED_SAMPLE_STATES:
            return self.log("Cannot import results, sample state: %s" % state)

        # get the suitable analyses of the sample, grouped by keyword
        if not self.analyses_by_keyword:
            sample_id = api.get_id(self.sample)
            return self.log("Cannot import results, no analyses left for "
                            "sample %s" % sample_id)

        # iterate over astm results and try to import them
        attach = False
        for result in self.get_results():
            imported = self.import_result(result)
            if imported:
                attach = True

        # create a new attachment with the message contents
        if attach:
            sender = self.get_sender()
            filename = "%s.txt" % "_".join(sender)
            attachment = self.create_attachment(
                self.sample.getClient(), self.message, filename=filename
            )
            attachments = self.sample.getAttachment()
            if attachment not in attachments:
                attachments.append(attachment)
                self.sample.setAttachment(attachments)

    def get_analyses(self, term):
        """Returns analyses from the current sample for the given term
        """
        analyses = []
        # TODO Use a fieldset in Instrument instead of an instance property
        keywords = self.keywords_mapping.get(term, [term])
        if not isinstance(keywords, (list, tuple)):
            keywords = [keywords]
        for keyword in keywords:
            ans = self.analyses_by_keyword.get(keyword, [])
            analyses.extend(ans)
        return list(set(analyses))

    def get_captured_date(self, record):
        return record.get("completed_at")

    def get_test_id(self, record):
        test_id = record.get("test") or ""
        return test_id.strip()

    def get_test_result(self, record):
        value = record.get("value") or ""
        return value.strip()

    def get_test_interims(self, record):
        interims = record.get("interims") or []
        return copy.deepcopy(interims)

    def get_test_units(self, record):
        units = record.get("units") or ""
        return units.strip()

    def get_detection_limit_operand(self, record):
        """Returns the detection limit operand ('<' or '>') if present in the
        result record, unless already included in the result value
        """
        flag = record.get("abnormal_flag") or ""
        if flag in DL_OPERANDS:
            return flag
        return ""

    def import_result(self, record):
        """Tries to import the result (ASTM) for this sample
        """
        value = self.get_test_result(record)
        if not value:
            # skip empty results
            return False

        param = self.get_test_id(record)
        if not param:
            # skip no parameter found
            return False

        captured = self.get_captured_date(record)
        captured = dtime.to_DT(captured)
        if not captured:
            # skip no capture date found
            return False

        units = self.get_test_units(record)

        sample_id = api.get_id(self.sample)

        # try to resolve the keyword counterpart
        analyses = self.get_analyses(param)
        if not analyses:
            # skip, no analyses found for this keyword
            self.log("No analysis found for sample %s and parameter %s" %
                     (sample_id, param))
            return False

        if len(analyses) > 1:
            # skip, more than one analysis found
            self.log("More than one analysis found for sample %s and "
                     "parameter %s" % (sample_id, param))
            return False

        # resolve the basic settings of the analysis
        analysis = analyses[0]
        result_type = "string"
        if api.is_floatable(value):
            value = api.to_float(value)
            result_type = "numeric"

        # purge analysis
        # TODO Allow to configure this in a fieldset in Instrument
        analysis.setResultOptions([])
        analysis.setResultType(result_type)
        analysis.setUnitChoices([])
        analysis.setDetectionLimitOperand("")
        analysis.setAllowManualUncertainty(False)

        dl_operand = self.get_detection_limit_operand(record)
        if dl_operand:
            # We do want to store the detection limit, even if the manual
            # detection limit for the analysis is set to False
            analysis.setAllowManualDetectionLimit(True)
            analysis.setDetectionLimitOperand(dl_operand)

        # get the interims/result variables
        interims = self.get_test_interims(record)
        if interims:
            analysis.setInterimFields(interims)

        # set the result, capture date and unit
        analysis.setResult(value)
        analysis.setResultCaptureDate(captured)
        analysis.setUnit(units)

        # submit
        doActionFor(analysis, "submit")

        # report to the import log
        self.log("Imported result for sample %s and test %s: %s %s"
                 % (sample_id, param, value, units))

        return True
