# -*- coding: utf-8 -*-

from palau.lims.astm.sysmex import SysmexASTMImporter
from senaite.core.interfaces import IASTMImporter
from senaite.core.interfaces import ISenaiteCore
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


KEYWORDS_MAPPING = (
    # Tuple of (instrument_parameter, (service_keywords))
    ("HCT", ["HCT"]),
    ("HGB", ["Hb-"]),
    ("LYM#", ["LYMPH"]),
    ("LYM%", ["Lymphocytes"]),
    ("MCH", ["MCH"]),
    ("MCHC", ["MCHC"]),
    ("MCV", ["MCV"]),
    ("MPV", ["MPV"]),
    ("NEUT#", ["NEUT"]),
    ("NEUT%", ["Neutrophils"]),
    ("RBC", ["RBC_BF", "Red-CC", "RBC", "RPBC"]),
    ("WBC", ["WBC_BF", "White-CC", "WBC", "PWBC", "WC"]),
)


@adapter(Interface, Interface, ISenaiteCore)
@implementer(IASTMImporter)
class ASTMImporter(SysmexASTMImporter):
    """ASTM results importer for Sysmex XP-100
    """

    @property
    def keywords_mapping(self):
        return dict(KEYWORDS_MAPPING)
