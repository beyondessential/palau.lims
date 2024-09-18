# -*- coding: utf-8 -*-

from palau.lims.astm import ASTMBaseImporter as Base


KEYWORDS_MAPPING = (
    # Tuple of (instrument_parameter, (service_keywords))
    ("Crt", ["creat", "CREAT_A", "UCREA", "CREAT_V"]),
    ("Alb", ["Alb"]),
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
        patient = self.get_patient()
        if not patient:
            return default

        # Use patient record's practice_id
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
