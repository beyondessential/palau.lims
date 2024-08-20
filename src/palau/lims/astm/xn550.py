# -*- coding: utf-8 -*-

from bika.lims import api
from bika.lims.utils.analysis import get_significant_digits
from bika.lims.workflow import doActionFor
from senaite.core.api import dtime
from senaite.core.astm.importer import ASTMImporter as Base
from senaite.core.interfaces import IASTMImporter
from senaite.core.interfaces import ISenaiteCore
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer

ALLOWED_SAMPLE_STATES = ["sample_received"]

ALLOWED_ANALYSIS_STATES = ["unassigned", "assigned"]

KEYWORDS_MAPPING = (
    # Tuple of (instrument_parameter, (service_keywords))
    # TODO Move this into a fieldset in Instrument!!
    ("WBC", ["WBC_BF", "White-CC", "WBC", "PWBC", "WC"]),
    ("RBC", ["RBC_BF", "Red-CC", "RBC", "RPBC"]),
    ("HGB", ["Hb-"]),
    ("HCT", ["HCT"]),
    ("MCV", ["MCV"]),
    ("MCH", ["MCH"]),
    ("MCHC", ["MCHC"]),
    ("PLT", ["PLT"]),
    ("NEUT%", ["Neutrophils"]),
    ("LYMPH%", ["Lymphocytes"]),
    ("MONO%", ["Monocytes"]),
    ("EO%", ["Eosinophils"]),
    ("BASO%", ["Basophils"]),
    ("NEUT#", ["NEUT"]),
    ("LYMPH#", ["LYMPH"]),
    ("MONO#", ["MONO"]),
    ("EO#", ["EO"]),
    ("BASO#", ["BASO"]),
    #("RDW-SD", ),
    #("RDW-CV", ),
    #("PDW", ),
    ("MPV", ["MPV"]),
    #("P-LCR", ),
    #("PCT", ),
    #("RET%", ),
    ("RET#", ["Reticulocyte"]),
    #("IRF", ),
    #("LFR", ),
    #("MFR", ),
    #("HFR", ),
    #("LWBC", ),
)


@adapter(Interface, Interface, ISenaiteCore)
@implementer(IASTMImporter)
class ASTMImporter(Base):
    """ASTM results importer for Sysmex XN-550
    """

    def __init__(self, data, message, request):
        super(ASTMImporter, self).__init__(data, message, request)
        self._analyses_by_keyword = None

    def get_sample_id(self, default=None):
        """Get the Sample ID. For Sysmex XN, the 'sample_id' astm field from
        (O)rder record is not used, but 'instrument specimen id'
        """
        order = self.get_order()
        if not order:
            return default
        instrument = order.get("instrument")
        if not instrument:
            return default
        sid = instrument.get("sample_id").strip()
        if not sid:
            return default
        return sid

    @property
    def analyses_by_keyword(self):
        """Gets the analyses of the sample that are suitable for results input,
        grouped by keyword. Note that for a single keyword, more than one
        analysis can exist. Thus, a list for each keyword is returned
        """
        if not self.sample:
            return {}

        if self._analyses_by_keyword:
            return self._analyses_by_keyword

        self._analyses_by_keyword = {}
        brains = self.sample.getAnalyses(review_state=ALLOWED_ANALYSIS_STATES)
        for brain in brains:
            obj = api.get_object(brain)
            keyword = obj.getKeyword()
            self._analyses_by_keyword.setdefault(keyword, []).append(obj)
        return self._analyses_by_keyword

    def import_data(self):
        """Import Sysmex XN-550 Results
        """
        import pdb;pdb.set_trace()
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

        # iterate over astm results and try to find right analyses
        for result in self.get_results():
            self.import_result(result)

    def get_analyses(self, term):
        """Returns analyses from the current sample for the given term
        """
        analyses = []
        # TODO Move this into a fieldset in Instrument!!
        keywords = dict(KEYWORDS_MAPPING).get(term, default=[term])
        if not isinstance(keywords, (list, tuple)):
            keywords = [keywords]
        for keyword in keywords:
            ans = self.analyses_by_keyword.get(keyword, [])
            analyses.extend(ans)
        return list(set(analyses))

    def import_result(self, record):
        """Tries to import the result (ASTM) for this sample
        """
        value = record.get("value") or ""
        value = value.strip()
        if not value:
            # skip empty results
            return False

        test = record.get("test")
        if not test:
            # skip records without 'test' component
            return False

        param = test.get("parameter") or ""
        param = param.strip()
        if not param:
            # skip no parameter found
            return False

        captured = record.get("completed_at")
        captured = dtime.to_DT(captured)
        if not captured:
            # skip no capture date found
            return False

        units = record.get("units")

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
        precision = analysis.getPrecision()
        result_type = "string"
        if api.is_floatable(value):
            value = api.to_float(value)
            precision = get_significant_digits(value)
            result_type = "numeric"

        # purge analysis
        # TODO Allow to configure this in a fieldset in Instrument
        analysis.setResultOptions([])
        analysis.setResultType(result_type)
        analysis.setUnitChoices([])
        analysis.setDetectionLimitOperand("")
        #analysis.setLowerDetectionLimit("")
        #analysis.setUpperDetectionLimit("")
        analysis.setPrecision(precision)
        analysis.setAllowManualUncertainty(False)
        analysis.setPrecisionFromUncertainty(False)
        analysis.setUncertainties([])

        # set the result, unit
        analysis.setResult(value)
        analysis.setResultCaptureDate(captured)
        analysis.setUnit(units)

        # submit
        doActionFor(analysis, "submit")
