# -*- coding: utf-8 -*-

TAMANU_STORAGE = "senaite.tamanu.storage"

TAMANU_SEXES = (
    ("male", "m"),
    ("female", "f"),
    ("", ""),
)

LOINC_CODING_SYSTEM = "http://loinc.org"
SENAITE_TESTS_CODING_SYSTEM = "https://www.senaite.com/testCodes.html"
SENAITE_PROFILES_CODING_SYSTEM = "https://www.senaite.com/profileCodes.html"

LOINC_GENERIC_DIAGNOSTIC = {
    # Generic LOINC code 30954-2 (https://loinc.org/30954-2) that is used by
    # default in DiagnosticReport callbacks when no panel was defined in the
    # original Tamanu's ServiceRequest
    "system": "http://loinc.org",
    "code": " 30954-2",
    "display": "Relevant Dx tests/lab data"
}
