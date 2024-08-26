# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from palau.lims import messageFactory as _
from Products.Archetypes import DisplayList


TAMANU_ID = 'tamanu'

UNKNOWN_DOCTOR_FULLNAME = "Unknown doctor"

CULTURE_INTERPRETATION_KEYWORD = "CINTER"

LANG_SETTINGS = [
    # Site language
    ("default_language", "en"),
    # Available languages
    ("available_languages", ["en", "ja"]),
    # Show country-specific language variants
    # IMPORTANT: If True, .pot files for language variants are required
    ("use_combined_language_codes", False),
]

SETUP_SETTINGS = [
    ("title", "Setup"),
    # Security
    ("RestrictWorksheetUsersAccess", True),
    ("AllowToSubmitNotAssigned", True),
    ("RestrictWorksheetManagement", True),
    # Accounting
    ("ShowPrices", False),
    ("Currency", "USD"),
    ("DefaultCountry", "PW"),
    ("MemberDiscount", "0"),
    ("VAT", "10"),
    # Analyses
    ("CategoriseAnalysisServices", True),
    ("CategorizeSampleAnalyses", True),
    ("SampleAnalysesRequired", True),
    ("ExponentialFormatThreshold", "5"),
    ("EnableAnalysisRemarks", True),
    ("AutoVerifySamples", True),
    ("DefaultNumberOfARsToAdd", "1"),
    ("MaxNumberOfSamplesAdd", "10"),
    # Appearance
    ("ShowPartitions", True),
    # Sampling
    ("AutoreceiveSamples", True),
    # Sticker
    ("AutoPrintStickers", "receive"),
    ("DefaultNumberOfCopies", "3"),
    ("AutoStickerTemplate", "palau.lims.stickers:Code_39_70x20mm"),
    ("SmallStickerTemplate", "palau.lims.stickers:QR_1x14mmx39mm"),
    ("LargeStickerTemplate", "palau.lims.stickers:Code_39_70x20mm"),
]

LABORATORY_ADDRESS = {
    "address": "MHHS P.O. Box 6027 Koror, Republic of Palau 96940",
    "zip": "",
    "city": "Abuja",
    "district": "",
    "state": "Koror",
    "country": "Palau",
}

LABORATORY_SETTINGS = [
    ("title", "Belau National Hospital Laboratory"),
    ("Name", "Belau National Hospital Laboratory"),
    ("PhysicalAddress", LABORATORY_ADDRESS),
    ("PostalAddress", LABORATORY_ADDRESS),
    ("BillingAddress", LABORATORY_ADDRESS),
    ("Phone", "(680) 488- 6100"),
    ("Fax", "(680) 488-1211"),
    ("EmailAddress", "administration@palauhealth.org"),
    ("LabURL", "www.palauhealth.org"),
]

IMPRESS_SETTINGS = [
    ("templates", ["palau.lims.impress:Default.pt", ]),
    ("default_template", "palau.lims.impress:Default.pt"),
]

PATIENT_SETTINGS = [
    ("senaite.patient.gender_visible", False),
    ("senaite.patient.age_supported", False),
    ("senaite.patient.patient_entry_mode", "first_last"),
]

REJECTION_REASONS = (
    "Unsuitable specimen container",
    "Insufficient specimen collected",
    "Specimen contaminated",
    "Labelling error",
    "Unlabelled",
    "Specimen received in syringe",
    "No specimen received",
    "No lab request form",
    "Leakage during transit",
    "Please recollect if clinically indicated",
)

# Tuples of (id, folder_id)
# If folder_id is None, assume folder_id is portal
ACTIONS_TO_HIDE = [
]

# An array of dicts. Each dict represents an ID formatting configuration
ID_FORMATTING = [
    {
        "portal_type": "AnalysisRequest",
        "form": "{clientId}{sampleType}{year}{alpha:1a3d}",
        "prefix": "analysisrequest",
        "sequence_type": "generated",
        # Split length is the number of elements to join without taking the
        # 'separator' (default '-') into account. Thus, for a format like
        # AR-{sampleType}-{parentId}{alpha:3a2d}, the suitable split_length
        # should be 3, so the parts "AR", "{sampleType}" and "{parentId}" are
        # joined together as the prefix template ("AR-{sampleType}{parentId}",
        # so the last part ({alpha:3a2d}) becomes computed each time.
        "split_length": 1,
    }, {
        "portal_type": "AnalysisRequestPartition",
        "form": "{parent_ar_id}P{partition_count:01d}",
        "prefix": "analysisrequestpartition",
        "sequence_type": "",
        "split-length": 1
    }, {
        "portal_type": "AnalysisRequestRetest",
        "form": "{parent_base_id}R{retest_count:01d}",
        "prefix": "analysisrequestretest",
        "sequence_type": "",
        "split-length": 1
    }, {
        "portal_type": "AnalysisRequestSecondary",
        "form": "{parent_ar_id}S{secondary_count:01d}",
        "prefix": "analysisrequestsecondary",
        "sequence_type": "",
        "split-length": 1
    }, {
        "portal_type": "Worksheet",
        "form": "WS{yymmdd}-{seq:02d}",
        "prefix": "worksheet",
        "sequence_type": "generated",
        "split_length": 2,
    }, {
        "portal_type": "MedicalRecordNumber",
        "form": "TA{seq:06d}",
        "prefix": "medicalrecordnumber",
        "sequence_type": "generated",
        "split_length": 1,
    }
]

# List of field names to not display in Sample Add form
SAMPLE_ADD_FIELDS_TO_HIDE = [
    "CCContact",
    "CCEmails",
    "Batch",
    "InternalUse",
    "Preservation",
    "SampleCondition",
    "DateOfAdmission",
    "PatientAddress",
    "Template",
    "EnvironmentalConditions",
    "Preservation",
    "SamplingDate",
    "SamplePoint",
    "ClientSampleID",
]

# Display order of Sample fields
SAMPLE_FIELDS_ORDER = [
    "PrimaryAnalysisRequest",
    "Batch",
    "Client",
    "Contact",
    "CCContact",
    "CCEmails",
    "MedicalRecordNumber",
    "PatientFullName",
    "PatientAddress",
    "DateOfBirth",
    "Sex",
    "Gender",
    "SamplingDate",
    "DateSampled",
    "DateOfAdmission",
    "WardDepartment",
    "Ward",
    "Location",
    "ClinicalInformation",
    "CurrentAntibiotics",
    "SampleType",
    "SampleCondition",
    "Profiles",
    "Template",
    "Container",
    "Bottles",
    "Preservation",
    "Volume",
    "SamplePoint",
    "Site",
    "EnvironmentalConditions",
    "Priority",
    "InternalUse",
    "RejectionReasons",
    "Remarks",
    "_ARAttachment",
    "NumSamples",
    "Specification",
]

# List of an analysis status to be reported in results
ANALYSIS_REPORTABLE_STATUSES = (
    "to_be_verified",
    "verified",
    "published",
    "out_of_stock",
)

LOCATIONS = DisplayList((
    ("int", _("Inpatient")),
    ("out", _("Outpatient")),
    ("", _("Not specified")),
))

PRIORITIES = DisplayList((
    ("1", _("Stat")),
    ("3", _("Asap")),
    ("5", _("Routine")),
))

TARGET_PATIENTS = DisplayList((
    ("a", _("Adult patient")),
    ("p", _("Paediatric patient")),
))

MONTHS = {
    1: _("January"),
    2: _("February"),
    3: _("March"),
    4: _("April"),
    5: _("May"),
    6: _("June"),
    7: _("July"),
    8: _("August"),
    9: _("September"),
    10: _("October"),
    11: _("November"),
    12: _("December")
}
