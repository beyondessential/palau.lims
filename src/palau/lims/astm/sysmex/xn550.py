# -*- coding: utf-8 -*-

from palau.lims.astm.sysmex import SysmexASTMImporter
from senaite.core.interfaces import IASTMImporter
from senaite.core.interfaces import ISenaiteCore
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


KEYWORDS_MAPPING = (
    # Tuple of (instrument_parameter, (service_keywords))
    ("BASO#", ["BASO"]),
    ("BASO%", ["Basophils"]),
    ("EO#", ["EO"]),
    ("EO%", ["Eosinophils"]),
    ("HCT", ["HCT"]),
    ("HGB", ["Hb-"]),
    ("IG#", ["IG"]),
    ("IG%", ["ig"]),
    ("LYMPH#", ["LYMPH"]),
    ("LYMPH%", ["Lymphocytes"]),
    ("MCH", ["MCH"]),
    ("MCHC", ["MCHC"]),
    ("MCV", ["MCV"]),
    ("MONO#", ["MONO"]),
    ("MONO%", ["Monocytes"]),
    ("MPV", ["MPV"]),
    ("NEUT#", ["NEUT"]),
    ("NEUT%", ["Neutrophils"]),
    ("PLT", ["PLT"]),
    ("RBC", ["RBC_BF", "Red-CC", "RBC", "RPBC"]),
    ("RET#", ["Reticulocyte"]),
    ("WBC", ["WBC_BF", "White-CC", "WBC", "PWBC", "WC"]),
)


@adapter(Interface, Interface, ISenaiteCore)
@implementer(IASTMImporter)
class ASTMImporter(SysmexASTMImporter):
    """ASTM results importer for Sysmex XN-550
    """

    @property
    def keywords_mapping(self):
        return dict(KEYWORDS_MAPPING)
