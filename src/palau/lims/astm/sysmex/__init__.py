# -*- coding: utf-8 -*-

from palau.lims.astm import ASTMBaseImporter as Base


class SysmexASTMImporter(Base):
    """Basic ASTM results importer for Sysmex instruments
    """

    def get_sample_id(self, default=None):
        """Get the Sample ID. For Sysmex, the 'sample_id' astm field from
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

    def get_test_id(self, record):
        """Returns the test ID from the given results record
        """
        test = record.get("test") or {}
        param = test.get("parameter") or ""
        return param.strip()
