# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import copy

from AccessControl import Unauthorized
from bika.lims import api
from bika.lims import deprecated
from bika.lims.api import security
from bika.lims.browser.analysisrequest.add2 import AR_CONFIGURATION_STORAGE
from bika.lims.interfaces import ISubmitted
from bika.lims.interfaces import IVerified
from bika.lims.vocabularies import getStickerTemplates
from bika.lims.workflow import doActionFor
from bika.lims.workflow import isTransitionAllowed
from BTrees.OOBTree import OOBTree
from plone import api as ploneapi
from plone.registry.interfaces import IRegistry
from palau.lims import logger
from palau.lims import permissions
from palau.lims import PRODUCT_NAME
from palau.lims import PROFILE_ID
from palau.lims.config import ANTIBIOTICS
from palau.lims.config import AST_PANELS
from palau.lims.config import CONTAINER_TYPES
from palau.lims.config import CONTAINERS
from palau.lims.config import MICROORGANISMS
from palau.lims.config import PRESERVATIONS
from palau.lims.config import PROFILES
from palau.lims.config import SAMPLE_FIELDS_ORDER
from palau.lims.config import SAMPLE_POINTS
from palau.lims.config import SAMPLE_TYPES
from palau.lims.config import SERVICES
from palau.lims.config import SPECIFICATIONS
from palau.lims.config import WARDS
from palau.lims.utils import get_field_value
from palau.lims.utils import get_file_resource
from palau.lims.utils import is_unknown_doctor
from palau.lims.utils import read_csv
from palau.lims.utils import set_field_value
from palau.lims.workflow.client import create_unknown_doctor
from Products.Archetypes.utils import mapply
from Products.CMFCore.permissions import ModifyPortalContent
from Products.DCWorkflow.Guard import Guard
from senaite.ast.calc import update_sensitivity_result
from senaite.ast.config import IDENTIFICATION_KEY
from senaite.ast.config import REPORT_EXTRAPOLATED_KEY
from senaite.ast.config import REPORT_KEY
from senaite.ast.config import SERVICES_SETTINGS
from senaite.core.catalog import ANALYSIS_CATALOG
from senaite.core.catalog import SAMPLE_CATALOG
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.setuphandlers import setup_core_catalogs
from senaite.core.setuphandlers import setup_other_catalogs
from senaite.core.workflow import SAMPLE_WORKFLOW
from senaite.core.permissions import FieldEditRemarks
from senaite.patient import ISenaitePatientLayer
from senaite.patient.subscribers.analysisrequest import update_patient
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

# Add-on specific Catalogs (list of core's BaseCatalog objects)
CATALOGS = (
)

# Tuples of (type, [catalog])
CATALOGS_BY_TYPE = [
]

# Tuples of (catalog, index_name)
INDEXES_TO_REMOVE = [
]

# Tuples of (catalog, column_name)
COLUMNS_TO_REMOVE = [
]

# Tuples of (catalog, index_name, index_attribute, index_type)
INDEXES = [
    (SAMPLE_CATALOG, "is_temporary_mrn", "", "BooleanIndex"),
    (SAMPLE_CATALOG, "medical_record_number", "", "KeywordIndex"),
    (ANALYSIS_CATALOG, "date_sampled", "", "DateIndex"),
]

# Tuples of (catalog, column_name)
COLUMNS = [
    (SAMPLE_CATALOG, "isMedicalRecordTemporary"),
]

# Tuples of (field_name, value)
SETUP_SETTINGS = [
    ("title", "Png"),
    ("DefaultCountry", "PG"),
    ("DefaultNumberOfARsToAdd", 1),
    ("ShowPartitions", True),
    ("EnableAnalysisRemarks", True),
    ("AutoStickerTemplate", "palau.lims.stickers: Code 39 40x20mm"),
    ("SmallStickerTemplate", "palau.lims.stickers: QR_1x14mmx39mm"),
    ("LargeStickerTemplate", "palau.lims.stickers: Code 39 40x20mm"),
]

# Tuples of (field_name, value)
IMPRESS_SETTINGS = [
    ("templates", ["palau.lims.impress:Default.pt", ]),
    ("default_template", "palau.lims.impress:Default.pt"),
]

# Tuples of (field_name, value)
PATIENT_SETTINGS = [
    ("senaite.patient.gender_visible", False),
    ("senaite.patient.patient_entry_mode", "first_last"),
]

# Tuples of (id, folder_id)
# If folder_id is None, assume folder_id is portal
ACTIONS_TO_HIDE = [
    ("supplyorders", None),
    ("patients", None),
]

# Skin layers that have priority over others, sorted from more to less priority
SORTED_SKIN_LAYERS = [
    "custom",
    "palau.lims",
    "bika"
]

# List of field names to not display in Sample Add form
SAMPLE_ADD_FIELDS_TO_HIDE = [
    "Remarks",
    "CCContact",
    "CCEmails",
    "Batch",
    "InternalUse",
    "Preservation",
    "SampleCondition",
]

# An array of dicts. Each dict represents an ID formatting configuration
ID_FORMATTING = [
    {
        "portal_type": "AnalysisRequest",
        "form": "{year}{alpha:2a3d}",
        "prefix": "analysisrequest",
        "sequence_type": "generated",
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

# Tuples of ID, Title, FTI
SETUP_FOLDERS = [
    ("wards", "Wards", "Wards"),
    ("clinicalinformations", "Clinical Informations", "ClinicalInformations"),
    ("warddepartments", "Ward Departments", "WardDepartments"),
]

# Tuples of (portal_type, list of behaviors)
BEHAVIORS = [
    ("SampleContainer", [
        "palau.lims.behaviors.samplecontainer.IExtendedSampleContainerBehavior",
    ])
]

# Workflow updates
WORKFLOWS_TO_UPDATE = {
    SAMPLE_WORKFLOW: {
        "states": {
            "verified": {
                "preserve_transitions": True,
                "permissions": {
                    # Field permissions (read-only)
                    permissions.FieldEditBottles: (),
                    permissions.FieldEditClinicalInformation: (),
                    permissions.FieldEditCurrentAntibiotics: (),
                    permissions.FieldEditVolume: (),
                    permissions.FieldEditWard: (),
                    permissions.FieldEditWardDepartment: (),
                    permissions.FieldEditLocation: (),
                }
            },
            "published": {
                "preserve_transitions": True,
                "transitions": ("create_supplementary",),
                "permissions": {
                    # Field permissions (read-only)
                    permissions.FieldEditBottles: (),
                    permissions.FieldEditClinicalInformation: (),
                    permissions.FieldEditCurrentAntibiotics: (),
                    permissions.FieldEditVolume: (),
                    permissions.FieldEditWard: (),
                    permissions.FieldEditWardDepartment: (),
                    permissions.FieldEditLocation: (),
                    permissions.FieldEditDateOfAdmission: (),
                }
            },
            "rejected": {
                "preserve_transitions": True,
                "permissions": {
                    # Field permissions (read-only)
                    permissions.FieldEditBottles: (),
                    permissions.FieldEditClinicalInformation: (),
                    permissions.FieldEditCurrentAntibiotics: (),
                    permissions.FieldEditVolume: (),
                    permissions.FieldEditWard: (),
                    permissions.FieldEditLocation: (),
                    FieldEditRemarks: ("LabClerk", "LabManager"),
                    permissions.FieldEditWardDepartment: (),
                    permissions.FieldEditDateOfAdmission: (),
                }
            },
            "invalid": {
                "preserve_transitions": True,
                "permissions": {
                    # Field permissions (read-only)
                    permissions.FieldEditBottles: (),
                    permissions.FieldEditClinicalInformation: (),
                    permissions.FieldEditCurrentAntibiotics: (),
                    permissions.FieldEditVolume: (),
                    permissions.FieldEditWard: (),
                    permissions.FieldEditLocation: (),
                    permissions.FieldEditWardDepartment: (),
                    permissions.FieldEditDateOfAdmission: (),
                }
            },
            "cancelled": {
                "preserve_transitions": True,
                "permissions": {
                    # Field permissions (read-only)
                    permissions.FieldEditBottles: (),
                    permissions.FieldEditClinicalInformation: (),
                    permissions.FieldEditCurrentAntibiotics: (),
                    permissions.FieldEditVolume: (),
                    permissions.FieldEditWard: (),
                    permissions.FieldEditLocation: (),
                    permissions.FieldEditWardDepartment: (),
                    permissions.FieldEditDateOfAdmission: (),
                }
            }
        },
        "transitions": {
            "create_supplementary": {
                "title": "Create supplementary test",
                "new_state": "",
                "action": "Create supplementary test",
                "guard": {
                    "guard_permissions": permissions.TransitionCreateSupplementary,
                    "guard_roles": "",
                    "guard_expr": "python:here.guard_handler('create_supplementary')",
                }
            }
        }
    }
}


def setup_handler(context):
    """Generic setup handler
    """
    if context.readDataFile('palau.lims.txt') is None:
        return

    logger.info("{} setup handler [BEGIN]".format(PRODUCT_NAME.upper()))
    portal = context.getSite()

    # Setup catalogs
    setup_catalogs(portal)

    # Setup laboratory information
    setup_laboratory(portal)

    # Apply ID format to content types
    setup_id_formatting(portal)

    # Apply impress default settings
    setup_impress(portal)

    # Setup the sorting of skin layers
    setup_skin_layers(portal)

    # Add behaviors
    setup_behaviors(portal)

    # Setup workflows
    setup_workflows(portal)

    # Setup folders
    add_setup_folders(portal)

    # Configure visible navigation items
    setup_navigation_types(portal)

    # Hide actions from both navigation portlet and from control_panel
    hide_actions(portal)

    # Hide unused fields from Add Sample form
    hide_sample_add_fields(portal)

    # Sort fields from Add Sample form
    sort_sample_add_fields(portal)

    # Setup initial data
    #setup_wards(portal)
    #setup_sample_types(portal)
    #setup_sample_points(portal)
    #setup_container_types(portal)
    #setup_preservations(portal)
    #setup_containers(portal)
    #setup_unknown_doctors(portal)
    #setup_analysis_services(portal)
    #setup_profiles(portal)
    #setup_specifications(portal)
    #setup_microorganisms(portal)
    #setup_antibiotics(portal)
    #setup_ast_panels(portal)

    # Walk-through existing samples and create missing Patients
    #create_missing_patients(portal)

    # Fix Sample current Antibiotics
    # fix_sample_current_antibiotics(portal)

    # Fix Sample Clinical informations
    # fix_sample_clinical_informations(portal)

    # Add multiselect interim for AST's Microorganism identification to allow
    # the introduction of growth number required for "BD EpiCenter"
    # https://github.com/beyondessential/pnghealth.lims/issues/170
    update_ast_identification(portal)

    # Set the default interims for AST selective reporting analyses
    # fix_default_selective_reporting(portal)

    # Fix AST analysis results for which extrapolated analysis reporting
    # selective test was dismissed when calculating the final result
    # See https://github.com/senaite/senaite.core/pull/1999/
    # fix_dismissed_extrapolated_results(portal)

    # Setup default settings for senaite.patient add-on
    setup_patient_settings(portal)

    # Setup default stickers
    # https://github.com/beyondessential/pnghealth.lims/issues/299
    setup_default_stickers(portal)

    # Update edit permission for all AST analysis services
    setup_ast_services_permission(portal)

    logger.info("{} setup handler [DONE]".format(PRODUCT_NAME.upper()))


def pre_install(portal_setup):
    """Runs before the first import step of the *default* profile
    This handler is registered as a *pre_handler* in the generic setup profile
    :param portal_setup: SetupTool
    """
    logger.info("{} pre-install handler [BEGIN]".format(PRODUCT_NAME.upper()))
    context = portal_setup._getImportContext(PROFILE_ID)
    portal = context.getSite()  # noqa

    logger.info("{} pre-install handler [DONE]".format(PRODUCT_NAME.upper()))


def post_install(portal_setup):
    """Runs after the last import step of the *default* profile
    This handler is registered as a *post_handler* in the generic setup profile
    :param portal_setup: SetupTool
    """
    logger.info("{} install handler [BEGIN]".format(PRODUCT_NAME.upper()))
    context = portal_setup._getImportContext(PROFILE_ID)
    portal = context.getSite()  # noqa

    logger.info("{} install handler [DONE]".format(PRODUCT_NAME.upper()))


def post_uninstall(portal_setup):
    """Runs after the last import step of the *uninstall* profile
    This handler is registered as a *post_handler* in the generic setup profile
    :param portal_setup: SetupTool
    """
    logger.info("{} uninstall handler [BEGIN]".format(PRODUCT_NAME.upper()))

    # https://docs.plone.org/develop/addons/components/genericsetup.html#custom-installer-code-setuphandlers-py
    profile_id = "profile-{}:uninstall".format(PRODUCT_NAME)
    context = portal_setup._getImportContext(profile_id)
    portal = context.getSite()  # noqa

    logger.info("{} uninstall handler [DONE]".format(PRODUCT_NAME.upper()))


def setup_laboratory(portal):
    """Setup Laboratory
    """
    logger.info("Setup Laboratory ...")
    setup = api.get_setup()

    # Apply general settings
    for field_name, value in SETUP_SETTINGS:
        set_field_value(setup, field_name, value)

    # Laboratory information
    lab = setup.laboratory
    lab.reindexObject()
    logger.info("Setup Laboratory [DONE]")


def setup_id_formatting(portal, format_definition=None):
    """Setup default ID formatting
    """
    if not format_definition:
        logger.info("Setting up ID formatting ...")
        for formatting in ID_FORMATTING:
            setup_id_formatting(portal, format_definition=formatting)
        logger.info("Setting up ID formatting [DONE]")
        return

    bs = portal.bika_setup
    p_type = format_definition.get("portal_type", None)
    if not p_type:
        return

    form = format_definition.get("form", "")
    if not form:
        logger.info("Param 'form' for portal type {} not set [SKIP")
        return

    logger.info("Applying format '{}' for {}".format(form, p_type))
    ids = list()
    for record in bs.getIDFormatting():
        if record.get('portal_type', '') == p_type:
            continue
        ids.append(record)
    ids.append(format_definition)
    bs.setIDFormatting(ids)


def setup_skin_layers(portal):
    """Setup the sorting of skin layers
    """
    logger.info("Setup Skin layers ...")
    skins_tool = api.get_tool("portal_skins")
    selections = skins_tool._getSelections()

    # For each skin, resort the skins layers in accordande
    for skin_name in selections.keys():
        layers = selections[skin_name].split(",")
        filtered = filter(lambda layer: layer not in SORTED_SKIN_LAYERS, layers)
        new_layers = SORTED_SKIN_LAYERS + filtered
        selections[skin_name] = ",".join(new_layers)

    logger.info("Setup Skin layers [DONE]")


def hide_actions(portal):
    """Excludes actions from both navigation portlet and from control_panel
    """
    logger.info("Hiding actions ...")
    for action_id, folder_id in ACTIONS_TO_HIDE:
        if folder_id and folder_id not in portal:
            logger.info("{} not found in portal [SKIP]".format(folder_id))
            continue
        folder = folder_id and portal[folder_id] or portal
        hide_action(folder, action_id)


def hide_action(folder, action_id):
    logger.info("Hiding {} from {} ...".format(action_id, folder.id))
    if action_id not in folder:
        logger.info("{} not found in {} [SKIP]".format(action_id, folder.id))
        return

    item = folder[action_id]
    logger.info("Hide {} ({}) from nav bar".format(action_id, item.Title()))
    if api.is_dexterity_content(item):
        item.exclude_from_nav = True
    else:
        item.setExcludeFromNav(True)
    item.reindexObject()

    def get_action_index(action_id):
        for n, action in enumerate(cp.listActions()):
            if action.getId() == action_id:
                return n
        return -1

    logger.info("Hide {} from control_panel".format(action_id, item.Title()))
    cp = api.get_tool("portal_controlpanel")
    action_index = get_action_index(action_id)
    if action_index == -1:
        logger.info("{}  not found in control_panel [SKIP]".format(cp.id))
        return

    actions = cp._cloneActions()
    del actions[action_index]
    cp._actions = tuple(actions)
    cp._p_changed = 1


def reindex_content_structure(portal):
    """Reindex contents generated by Generic Setup
    """
    logger.info("Reindex content structure ...")
    to_hide = dict(ACTIONS_TO_HIDE).keys()
    for obj in portal.objectValues():
        if not api.is_object(obj):
            continue
        if api.get_id(obj) in to_hide:
            continue
        logger.info("Reindexing {}".format(repr(obj)))
        if hasattr(obj, "setExpirationDate"):
            obj.setExpirationDate(None)
        if hasattr(obj, "setExcludeFromNav"):
            obj.setExcludeFromNav(False)
        else:
            obj.exclude_from_nav = False
        obj.reindexObject()

    logger.info("Reindex content structure [DONE]")


def get_manage_add_storage(portal):
    setup = portal.bika_setup
    annotation = IAnnotations(setup)
    storage = annotation.get(AR_CONFIGURATION_STORAGE)
    if storage is None:
        annotation[AR_CONFIGURATION_STORAGE] = OOBTree()
    return annotation[AR_CONFIGURATION_STORAGE]


def update_manage_add_storage(portal, storage):
    setup = portal.bika_setup
    annotation = IAnnotations(setup)
    annotation[AR_CONFIGURATION_STORAGE] = storage


def hide_sample_add_fields(portal):
    """Hides unused fields from Sample Add Form
    """
    logger.info("Hiding default fields from Sample Add ...")
    storage = get_manage_add_storage(portal)
    visibility = storage.get('visibility', {}).copy()
    ordered = SAMPLE_FIELDS_ORDER
    fields = list(set(visibility.keys() + SAMPLE_ADD_FIELDS_TO_HIDE + ordered))
    for field_name in fields:
        visibility[field_name] = field_name not in SAMPLE_ADD_FIELDS_TO_HIDE
    storage.update({"visibility": visibility})
    update_manage_add_storage(portal, storage)
    logger.info("Hiding default fields from Sample Add [DONE]")


def sort_sample_add_fields(portal):
    """Sort Sample fields from Sample Add Form
    """
    logger.info("Sorting fields from Sample Add ...")
    storage = get_manage_add_storage(portal)
    storage.update({"order": SAMPLE_FIELDS_ORDER})
    update_manage_add_storage(portal, storage)
    logger.info("Sorting fields from Sample Add [DONE]")


def add_setup_folders(portal):
    """Adds the initial folders in setup
    """
    logger.info("Adding setup folders ...")

    setup = api.get_setup()
    pt = api.get_tool("portal_types")
    ti = pt.getTypeInfo(setup)

    # get the current allowed types for the object
    allowed_types = ti.allowed_content_types

    def show_in_nav(obj):
        if hasattr(obj, "setExpirationDate"):
            obj.setExpirationDate(None)
        if hasattr(obj, "setExcludeFromNav"):
            obj.setExcludeFromNav(False)

    for folder_id, folder_name, portal_type in SETUP_FOLDERS:
        obj = setup.get(folder_id)
        if obj:
            # Object exists already
            show_in_nav(obj)
        else:
            # append the allowed type
            ti.allowed_content_types = allowed_types + (portal_type, )

            logger.info("Adding folder: {}".format(folder_id))
            setup.invokeFactory(portal_type, folder_id, title=folder_name)
            obj = setup.get(folder_id)

        show_in_nav(obj)

    # reset the allowed content types
    ti.allowed_content_types = allowed_types

    logger.info("Adding setup folders [DONE]")


def setup_navigation_types(portal):
    """Add additional types for navigation
    """
    logger.info("Setup navigation types ...")
    registry = getUtility(IRegistry)
    key = "plone.displayed_types"
    display_types = registry.get(key, ())

    new_display_types = set(display_types)
    to_display = map(lambda f: f[2], SETUP_FOLDERS)
    new_display_types.update(to_display)
    registry[key] = tuple(new_display_types)
    logger.info("Setup navigation types [DONE]")


def setup_wards(portal):
    """Setup default Wards
    """
    logger.info("Setup Wards ...")
    folder = api.get_setup().wards
    folder_title = api.get_title(folder)
    for name, settings in WARDS:
        logger.info("Setup ward '{}' ...".format(name))
        exists = filter(lambda s: api.get_title(s) == name, folder.objectValues())
        if exists:
            logger.info("Ward '{}' exists already".format(name))
            continue

        ward = api.create(folder, "Ward", title=name)
        ward.description = settings["description"]
        ward.reindexObject()

    # After adding objects, the folder loose the title
    folder.title = folder_title
    folder.reindexObject()

    logger.info("Setup Culture services [DONE]")


def setup_analysis_services(portal):
    """Setup the analysis services
    """
    logger.info("Setup Analysis services ...")
    for key, settings in SERVICES.items():
        logger.info("Setup service '{}' ...".format(key))
        folder = api.get_setup().bika_analysisservices
        exists = filter(lambda s: s.getKeyword() == key, folder.objectValues())
        if exists:
            logger.info("Service '{}' exists already".format(key))
            continue

        # Get/create the category
        cat_name = settings["Category"]
        cat_folder = api.get_setup().bika_analysiscategories
        categories = cat_folder.objectValues()
        category = filter(lambda c: api.get_title(c) == cat_name, categories)
        if not category:
            logger.info("Setup category '{}' ...".format(cat_name))
            category = api.create(cat_folder, "AnalysisCategory",
                                  title=cat_name)
        else:
            category = category[0]

        title = settings["title"]
        service = api.create(folder, "AnalysisService", Category=category,
                             title=title, Keyword=key)
        unit = settings.get("Unit", "")
        service.setUnit(unit)
        result_options = settings.get("ResultOptions")
        if result_options:
            options = map(lambda r: {"ResultValue": r[0],
                                     "ResultText": r[1],
                                     "Flag": r[2]}, result_options)
            service.setResultOptions(options)

        result_options_type = settings.get("ResultOptionsType")
        if result_options_type:
            service.setResultOptionsType(result_options_type)

    logger.info("Setup Analysis services [DONE]")


def setup_profiles(portal):
    """Setup the analysis services
    """
    logger.info("Setup Analysis profiles ...")
    for title, settings in PROFILES:
        key = settings["ProfileKey"]
        logger.info("Setup profile '{} - {}' ...".format(key, title))
        folder = api.get_setup().bika_analysisprofiles
        existing = folder.objectValues()
        exists = filter(lambda p: p.getProfileKey() == key, existing)
        if exists:
            logger.info("Profile with key '{}' exists already".format(key))
            continue

        # Get the services
        keywords = settings["Service"]
        query = {"portal_type": "AnalysisService", "getKeyword": keywords}
        services = api.search(query, SETUP_CATALOG)
        services_uids = map(api.get_uid, services)

        # Create the profile
        profile = api.create(folder, "AnalysisProfile", ProfileKey=key,
                             title=title)
        profile.setService(services_uids)

    logger.info("Setup Analysis profiles [DONE]")


def setup_specifications(portal):
    """Setup the analysis specifications
    """
    logger.info("Setup Analysis specifications ...")
    for title, settings in SPECIFICATIONS:
        logger.info("Setup specifications '{}' ...".format(title))
        folder = api.get_setup().bika_analysisspecs
        existing = folder.objectValues()
        exists = filter(lambda s: api.get_title(s) == title, existing)
        if exists:
            logger.info("Specification '{}' exists already".format(title))
            continue

        # Get the sample type
        st_prefix = settings["SampleType"]
        sts = api.get_setup().bika_sampletypes.objectValues()
        st = filter(lambda s: s.getPrefix() == st_prefix, sts)
        sample_type = st and st[0] or None
        if not sample_type:
            logger.error("Sample Type '{}' is missing!".format(st_prefix))
            continue

        # Build the results range
        result_ranges = []
        for key, result_range in settings["ResultsRange"].items():
            query = {"portal_type": "AnalysisService", "getKeyword": key}
            service = api.search(query, SETUP_CATALOG)[0]
            rr = copy.deepcopy(result_range)
            rr.update({"uid": api.get_uid(service), "keyword": key})
            result_ranges.append(rr)

        # Create the analysis specifications
        api.create(folder, "AnalysisSpec", title=title,
                   ResultsRange=result_ranges, SampleType=sample_type)

    logger.info("Setup Analysis specifications [DONE]")


def setup_microorganisms(portal):
    """Setup some microorganisms
    """
    logger.info("Setup Microorganisms ...")
    folder = api.get_setup().microorganisms
    folder_title = api.get_title(folder)
    for name, settings in MICROORGANISMS.items():
        logger.info("Setup microorganism '{}' ...".format(name))
        exists = filter(lambda s: api.get_title(s) == name, folder.objectValues())
        if exists:
            logger.info("Microorganism '{}' exists already".format(name))
            microorganism = exists[0]
        else:
            microorganism = api.create(folder, "Microorganism", title=name)
        microorganism.description = settings.get("description", "")
        microorganism.gram_stain = settings.get("gram_stain", None)
        microorganism.shape = settings.get("shape", None)
        microorganism.glass = settings.get("glass", False)
        microorganism.multi_resistant = settings.get("multi_resistant", False)
        microorganism.mro_phenotype = settings.get("mro_phenotype", "")
        if isTransitionAllowed(microorganism, "activate"):
            doActionFor(microorganism, "activate")
        microorganism.reindexObject()

    # After adding objects, the folder loose the title
    folder.title = folder_title
    folder.reindexObject()

    logger.info("Setup Culture services [DONE]")

def setup_antibiotics(portal):
    """Setup default antibiotics if do not exist yet
    """
    logger.info("Setup default antibiotics ...")

    # Get the titles of the existing antibiotics first
    folder = api.get_setup().get("antibiotics")
    existing = map(api.get_title, folder.objectValues())

    def get_antibiotic_class(name):
        query = {
            "portal_type": "AntibioticClass",
            "title": name,
        }
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            return api.get_object(brains[0])
        return None

    # Create the antibiotic classes
    for name, props in ANTIBIOTICS:
        if name in existing:
            logger.warn("Antibiotic {} already exists [SKIP]".format(name))
            continue

        logger.info("Adding antibiotic: {}".format(name))

        # Get the antibiotic class by name
        a_class_name = props.get("antibiotic_class")
        a_class = get_antibiotic_class(a_class_name)
        if not a_class:
            logger.error("Antibiotic class missing: '{}' [SKIP]".format(
                a_class_name))
            continue

        obj = api.create(folder, "Antibiotic", title=name)
        obj.description = props.get("description", "")
        obj.antibiotic_class = api.get_uid(a_class)
        obj.abbreviation = props.get("abbreviation")
        obj.reindexObject()

    # After adding the antibiotic, the folder looses the title
    folder.title = "Antibiotics"
    folder.reindexObject()
    logger.info("Setup default antibiotics [DONE]")


# TODO: Remove? Epicenter antibiotics have never been imported in production
# https://github.com/beyondessential/pnghealth.lims/pull/258
def setup_epicenter_antibiotics(portal):
    """Setup default antibiotics if do not exist yet
    """
    logger.info("Setup Epicenter Antibiotics ...")

    # extract the existing antibiotic classes
    setup = api.get_setup()
    wo_class = {}
    classes_folder = setup.antibiotic_classes
    classes = classes_folder.objectValues()
    classes = dict([(api.get_title(it), it.getId()) for it in classes])

    # extract the existing antibiotics
    folder = setup.antibiotics
    existing = folder.objectValues()
    existing = dict([(api.get_title(item), item.getId()) for item in existing])

    # read antibiotics from EpiCenter's organism table
    antibiotics_file = get_file_resource("epicenter_antibiotics.csv")
    antibiotics = read_csv(antibiotics_file)

    for info in antibiotics:
        name = info.get("Antimicrobial Name")
        logger.info("Setup antibiotic '{}' ...".format(name))

        # get legacy information from our config, if any
        legacy = dict(ANTIBIOTICS).get(name, {})
        legacy = copy.deepcopy(legacy)

        # resolve the class name giving priority to Epicenter's sub class
        class_choices = [
            info.get("Sub Class"),
            info.get("Class"),
            legacy.get("antibiotic_class"),
            "Other",
        ]
        class_name = filter(None, class_choices)[0]

        # TODO Add "SubClass" field to Antibiotic
        # XXX Note we use the Sub Class to populate SENAITE's Classes
        abx_class = None
        class_id = classes.get(class_name)
        if class_id:
            abx_class = classes_folder[class_id]
        elif class_name:
            # create the Antibiotic class, but only if non-empty
            abx_class = api.create(classes_folder, "AntibioticClass",
                                   title=class_name)
            classes.update({class_name: api.get_id(abx_class)})

        # find out if there are antibiotics w/o class
        for obj_uid in wo_class.pop(class_name, []):
            obj = api.get_object_by_uid(obj_uid)
            obj.antibiotic_class = api.get_uid(abx_class)

        # get the existing antibiotic or create a new one
        antibiotic_id = existing.get(name)
        if antibiotic_id:
            logger.info("Antibiotic '{}' exists already".format(name))
            antibiotic = folder[antibiotic_id]
        else:
            antibiotic = api.create(folder, "Antibiotic", title=name)

        # abbreviation = info.get("Abbreviation", organism.getAbbreviation())
        abbreviation = info.get("Abbreviation", "")

        # TODO Add "Code" field to Antibiotic
        # code = info.get("LIS Code", organism.getCode())
        code = info.get("LIS Code", "")

        # TODO Add "Group" field to Antibiotic
        group = info.get("Group", "")

        # TODO Add "SubGroup" field to Antibiotic
        sub_group = info.get("Sub Group", "")

        # resolve class
        class_uid = antibiotic.antibiotic_class
        if abx_class:
            class_uid = api.get_uid(abx_class)

        # update with additional info
        legacy.update({
            "abbreviation": abbreviation,
            "code": code or abbreviation,
            "description": antibiotic.description,
            "antibiotic_class": class_uid,
            "group": group,
            "sub_group": sub_group,
        })
        # update the object
        # TODO Use api.edit
        edit(antibiotic, **legacy)

        if isTransitionAllowed(antibiotic, "activate"):
            doActionFor(antibiotic, "activate")

        antibiotic.reindexObject()
        existing.update({name: api.get_id(antibiotic)})

        if not abx_class:
            uid = api.get_uid(antibiotic)
            wo_class.setdefault(name, []).append(uid)

    logger.info("Setup Epicenter Antibiotics [DONE]")


@deprecated("Use senaite.core.api.edit instead")
def edit(obj, check_permissions=True, **kwargs):
    """Updates the values of object fields with the new values passed-in
    """
    # Prevent circular dependencies
    from bika.lims.api.security import check_permission
    fields = api.get_fields(obj)
    for name, value in kwargs.items():
        field = fields.get(name, None)
        if not field:
            continue

        # cannot update readonly fields
        readonly = getattr(field, "readonly", False)
        if readonly:
            raise ValueError("Field '{}' is readonly".format(name))

        # check field writable permission
        if check_permissions:
            perm = getattr(field, "write_permission", ModifyPortalContent)
            if perm and not check_permission(perm, obj):
                raise Unauthorized("Field '{}' is not writeable".format(name))

        # Set the value
        if hasattr(field, "getMutator"):
            mutator = field.getMutator(obj)
            mapply(mutator, value)
        else:
            field.set(obj, value)


def setup_ast_panels(portal):
    """Setup default AST Panels if do not exist yet
    """
    logger.info("Setup default AST Panels ...")

    # Get the titles of the existing antibiotics first
    folder = api.get_setup().get("astpanels")
    folder_title = api.get_title(folder)

    def get_object(query):
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            return api.get_object(brains[0])
        return None

    def get_microorganism(name):
        query = {
            "portal_type": "Microorganism",
            "title": name,
        }
        return get_object(query)

    def get_antibiotic(name):
        query = {
            "portal_type": "Antibiotic",
            "title": name,
        }
        return get_object(query)

    def get_panel(name):
        query = {
            "portal_type": "ASTPanel",
            "title": name,
        }
        return get_object(query)

    # Create the AST panels
    for name, props in AST_PANELS:
        logger.info("Adding AST Panel: {}".format(name))

        # Get the microorganisms by name
        microorganisms = props.get("microorganisms")
        microorganisms = filter(None, map(get_microorganism, microorganisms))
        microorganisms = map(api.get_uid, microorganisms)

        # Get the antibiotics by name
        antibiotics = props.get("antibiotics")
        antibiotics = filter(None, map(get_antibiotic, antibiotics))
        antibiotics = map(api.get_uid, antibiotics)

        obj = get_panel(name)
        if obj:
            logger.warn("AST Panel '{}' already exists".format(name))
        else:
            obj = api.create(folder, "ASTPanel", title=name)

        obj.microorganisms = microorganisms
        obj.antibiotics = antibiotics
        if isTransitionAllowed(obj, "activate"):
            doActionFor(obj, "activate")
        obj.reindexObject()

    # After adding the object, the folder looses the title
    folder.title = folder_title
    folder.reindexObject()
    logger.info("Setup default AST Panels [DONE]")


def setup_sample_types(portal):
    """Setup default Sample points
    """
    logger.info("Setup default Sample Types ...")
    folder = api.get_setup().bika_sampletypes
    existing = map(api.get_title, folder.objectValues())

    for name, props in SAMPLE_TYPES:
        if name in existing:
            logger.warn("Sample type '{}' already exists [SKIP]".format(name))
            continue

        logger.info("Adding Sample type: {}".format(name))
        obj = api.create(folder, "SampleType", title=name)
        obj.setDescription(props.get("description", ""))
        obj.setPrefix(props.get("prefix"))
        obj.setHazardous(props.get("hazardous", False))
        obj.setMinimumVolume(props.get("minimum_volume", "10 mL"))
        obj.setContainerWidget(props.get("container_widget"))
        obj.reindexObject()

    logger.info("Setup Sample Types [DONE]")


def setup_sample_points(portal):
    """Setup default Sample points
    """
    logger.info("Setup default Sample Points ...")
    folder = api.get_setup().bika_samplepoints
    existing = map(api.get_title, folder.objectValues())

    for name, props in SAMPLE_POINTS:
        if name in existing:
            logger.warn("Sample point '{}' already exists [SKIP]".format(name))
            continue

        logger.info("Adding Sample point: {}".format(name))
        obj = api.create(folder, "SamplePoint", title=name)
        obj.reindexObject()

    logger.info("Setup Sample Points [DONE]")


def setup_container_types(portal):
    """Setup default Container types
    """
    logger.info("Setup default Container types ...")
    folder = api.get_setup().bika_containertypes
    existing = map(api.get_title, folder.objectValues())

    for name, props in CONTAINER_TYPES:
        if name in existing:
            logger.warn("Container type '{}' already exists [SKIP]".format(name))
            continue

        logger.info("Adding Container type: {}".format(name))
        obj = api.create(folder, "ContainerType", title=name)
        obj.setDescription(props.get("description"))
        set_field_value(obj, "BACTECBottle", props.get("bactec", False))
        obj.reindexObject()

    logger.info("Setup Container types [DONE]")


def setup_preservations(portal):
    """Setup default Preservations
    """
    logger.info("Setup default Preservations ...")
    folder = api.get_setup().bika_preservations
    existing = map(api.get_title, folder.objectValues())

    for name, props in PRESERVATIONS:
        if name in existing:
            logger.warn(
                "Preservation '{}' already exists [SKIP]".format(name))
            continue

        logger.info("Adding Preservation: {}".format(name))
        obj = api.create(folder, "Preservation", title=name)
        obj.setDescription(props.get("description", ""))
        obj.reindexObject()

    logger.info("Setup Preservations [DONE]")


def setup_containers(portal):
    """Setup default Container types
    """
    logger.info("Setup default Containers ...")
    folder = api.get_setup().sample_containers
    existing = map(api.get_title, folder.objectValues())

    def get_object(name, portal_type="ContainerType"):
        if not name:
            return None
        query = {
            "portal_type": portal_type,
            "title": name,
        }
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            return api.get_object(brains[0])
        return None

    for name, props in CONTAINERS:
        if name in existing:
            logger.warn("Container '{}' already exists [SKIP]".format(name))
            obj_values = folder.objectValues()
            obj = filter(lambda ob: api.get_title(ob) == name, obj_values)[0]
            dry_weight = props.get("dry_weight")
            if dry_weight:
                set_field_value(obj, "weight", dry_weight)
            continue

        # Get the container type
        container_type_name = props.get("container_type")
        container_type = get_object(container_type_name, "ContainerType")
        if not container_type:
            logger.error("Container type is missing: '{}' [SKIP]".format(
                container_type_name))
            continue

        logger.info("Adding SampleContainer: {}".format(name))
        obj = api.create(folder, "SampleContainer", title=name)
        obj.setDescription(props.get("description"))
        obj.setCapacity(props.get("capacity"))
        obj.setContainerType(container_type)
        dry_weight = props.get("dry_weight")
        if dry_weight:
            set_field_value(obj, "weight", dry_weight)
        obj.reindexObject()

    logger.info("Setup Containers [DONE]")

def setup_unknown_doctors(portal):
    """Setup unknown doctors to those clients that do not have an Unknown
    Doctor yet
    """
    logger.info("Setting up unknown doctors ...")
    for client in portal.clients.objectValues("Client"):
        contacts = client.objectValues("Contact")
        unknown = filter(is_unknown_doctor, contacts)
        if not unknown:
            create_unknown_doctor(client)

    logger.info("Setting up unknown doctors [DONE]")


def setup_catalogs(portal):
    """Setup Plone catalogs
    """
    logger.info("Setup Catalogs ...")

    # Remove stale indexes
    remove_stale_indexes(portal)

    # Remove stale columns
    remove_stale_columns(portal)

    setup_core_catalogs(portal, catalog_classes=CATALOGS)
    setup_other_catalogs(portal, indexes=INDEXES, columns=COLUMNS)

    logger.info("Setup Catalogs [DONE]")


def remove_stale_indexes(portal):
    logger.info("Removing stale indexes ...")
    for catalog, index in INDEXES_TO_REMOVE:
        del_index(portal, catalog, index)


def remove_stale_columns(portal):
    logger.info("Removing stale columns ...")
    for catalog, col_id in COLUMNS_TO_REMOVE:
        del_column(catalog, col_id)


def del_index(portal, catalog_id, index_name):
    logger.info("Removing '{}' index from '{}' ..."
                .format(index_name, catalog_id))
    catalog = api.get_tool(catalog_id)
    if index_name not in catalog.indexes():
        logger.info("Index '{}' not in catalog '{}' [SKIP]"
                    .format(index_name, catalog_id))
        return
    catalog.delIndex(index_name)
    logger.info("Removing old index '{}' ...".format(index_name))


def del_column(catalog_id, name):
    """Removes the given metadata column from the catalog
    """
    logger.info("Removing '{}' column from '{}' ...".format(name, catalog_id))
    catalog = api.get_tool(catalog_id)
    if name not in catalog.schema():
        logger.info("Column '{}' not in catalog '{}' [SKIP]"
                    .format(name, catalog_id))
        return
    catalog.delColumn(name)
    logger.info("Column '{}' removed from '{}'".format(name, catalog_id))


def setup_workflows(portal):
    """Setup workflow changes (status, transitions, permissions, etc.)
    """
    logger.info("Setup workflows ...")
    for wf_id, settings in WORKFLOWS_TO_UPDATE.items():
        update_workflow(portal, wf_id, settings)
    logger.info("Setup workflows [DONE]")


def update_workflow(portal, workflow_id, settings):
    """Updates the workflow with workflow_id with the settings passed-in
    """
    logger.info("Updating workflow '{}' ...".format(workflow_id))
    wf_tool = api.get_tool("portal_workflow")
    workflow = wf_tool.getWorkflowById(workflow_id)
    if not workflow:
        logger.warn("Workflow '{}' not found [SKIP]".format(workflow_id))
    states = settings.get("states", {})
    for state_id, values in states.items():
        update_workflow_state(workflow, state_id, values)

    transitions = settings.get("transitions", {})
    for transition_id, values in transitions.items():
        update_workflow_transition(workflow, transition_id, values)


def update_workflow_state(workflow, status_id, settings):
    """Updates the status of a workflow in accordance with settings passed-in
    """
    logger.info("Updating workflow '{}', status: '{}' ..."
                .format(workflow.id, status_id))

    # Create the status (if does not exist yet)
    new_status = workflow.states.get(status_id)
    if not new_status:
        workflow.states.addState(status_id)
        new_status = workflow.states.get(status_id)

    # Set basic info (title, description, etc.)
    new_status.title = settings.get("title", new_status.title)
    new_status.description = settings.get("description", new_status.description)

    # Set transitions
    trans = settings.get("transitions", ())
    if settings.get("preserve_transitions", False):
        trans = tuple(set(new_status.transitions+trans))
    new_status.transitions = trans

    # Set permissions
    update_workflow_state_permissions(workflow, new_status, settings)


def update_workflow_state_permissions(workflow, status, settings):
    """Updates the permissions of a workflow status in accordance with the
    settings passed-in
    """
    # Copy permissions from another state?
    permissions_copy_from = settings.get("permissions_copy_from", None)
    if permissions_copy_from:
        logger.info("Copying permissions from '{}' to '{}' ..."
                    .format(permissions_copy_from, status.id))
        copy_from_state = workflow.states.get(permissions_copy_from)
        if not copy_from_state:
            logger.info("State '{}' not found [SKIP]".format(copy_from_state))
        else:
            for perm_id in copy_from_state.permissions:
                perm_info = copy_from_state.getPermissionInfo(perm_id)
                acquired = perm_info.get("acquired", 1)
                roles = perm_info.get("roles", acquired and [] or ())
                logger.info("Setting permission '{}' (acquired={}): '{}'"
                            .format(perm_id, repr(acquired), ', '.join(roles)))
                status.setPermission(perm_id, acquired, roles)

    # Override permissions
    logger.info("Overriding permissions for '{}' ...".format(status.id))
    state_permissions = settings.get('permissions', {})
    if not state_permissions:
        logger.info(
            "No permissions set for '{}' [SKIP]".format(status.id))
        return
    for permission_id, roles in state_permissions.items():
        if isinstance(roles, list):
            acq = 1
        elif isinstance(roles, tuple):
            acq = 0
        else:
            raise AttributeError("No valid perm: {}".format(permission_id))
        logger.info("Setting permission '{}' (acquired={}): '{}'"
                    .format(permission_id, repr(acq),
                            ', '.join(roles)))
        # Check if this permission is defined globally for this workflow
        if permission_id not in workflow.permissions:
            workflow.permissions = workflow.permissions + (permission_id, )
        status.setPermission(permission_id, acq, roles)


def update_workflow_transition(workflow, transition_id, settings):
    """Updates the workflow transition in accordance with settings passed-in
    """
    logger.info("Updating workflow '{}', transition: '{}'"
                .format(workflow.id, transition_id))
    if transition_id not in workflow.transitions:
        workflow.transitions.addTransition(transition_id)
    transition = workflow.transitions.get(transition_id)
    transition.setProperties(
        title=settings.get("title"),
        new_state_id=settings.get("new_state"),
        after_script_name=settings.get("after_script", ""),
        actbox_name=settings.get("action", settings.get("title"))
    )
    guard = transition.guard or Guard()
    guard_props = {"guard_permissions": "",
                   "guard_roles": "",
                   "guard_expr": ""}
    guard_props = settings.get("guard", guard_props)
    guard.changeFromProperties(guard_props)
    transition.guard = guard


def create_missing_patients(portal):
    """Walks through existing samples and creates missing Patients
    """
    logger.info("Creating missing patients ...")

    # Be sure the patient layer is active. Might happen senaite.patient add-on
    # gets installed while installing palau.lims, so the request does not provide
    # SenaitePatientLayer yet.
    request = api.get_request()
    alsoProvides(request, ISenaitePatientLayer)

    query = {"portal_type": "AnalysisRequest"}
    samples = api.search(query, SAMPLE_CATALOG)
    for brain in samples:
        sample = api.get_object(brain)

        # Create the patient if required
        update_patient(sample)

        # Reindex the sample to guarantee senaite.patient's indexes are
        # populated correctly
        sample.reindexObject()

    logger.info("Creating missing patients [DONE]")


def fix_sample_current_antibiotics(portal):
    """Walks through existing samples and resets current antibiotic field if
    it does not contain a list of uids.
    Tthe field was a text area before becoming a UIDReferenceField due to
    https://github.com/beyondessential/pnghealth.lims/issues/51
    """

    def get_antibiotic(name):
        query = {
            "portal_type": "Antibiotic",
            "title": name,
        }
        return get_object(query)

    def get_object(query):
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            return api.get_object(brains[0])
        return None

    logger.info("Fixing samples current antibiotics ...")
    query = {"portal_type": "AnalysisRequest"}
    samples = api.search(query, SAMPLE_CATALOG)
    for brain in samples:
        sample = api.get_object(brain)
        abx = get_field_value(sample, "CurrentAntibiotics")
        if not isinstance(abx, list):
            abx = filter(None, abx and [abx] or [])
            abx = filter(None, map(get_antibiotic, abx))
            abx = map(api.get_uid, abx)
            set_field_value(sample, "CurrentAntibiotics", abx)

    logger.info("Fixing samples current antibiotics [DONE]")


def fix_sample_clinical_informations(portal):
    """Walks through existing samples and resets current ClinicalInformation
    field if it does not contain a list of uids.
    Tthe field was a text area before becoming a UIDReferenceField due to
    https://github.com/beyondessential/pnghealth.lims/issues/52
    """

    def get_clinical_information(name):
        query = {
            "portal_type": "ClinicalInformation",
            "title": name,
        }
        return get_object(query)

    def get_object(query):
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            return api.get_object(brains[0])
        return None

    logger.info("Fixing samples clinical information ...")
    query = {"portal_type": "AnalysisRequest"}
    samples = api.search(query, SAMPLE_CATALOG)
    for brain in samples:
        sample = api.get_object(brain)
        info = get_field_value(sample, "ClinicalInformation")
        if not isinstance(info, list):
            info = filter(None, info and [info] or [])
            info = filter(None, map(get_clinical_information, info))
            info = map(api.get_uid, info)
            set_field_value(sample, "ClinicalInformation", info)

    logger.info("Fixing samples clinical information [DONE]")


def setup_impress(portal):
    """Setup impress
    """
    logger.info("Setup Impress ...")
    for key, value in IMPRESS_SETTINGS:
        registry_id = "senaite.impress.{}".format(key)
        ploneapi.portal.set_registry_record(registry_id, value)
    logger.info("Setup Impress [DONE]")


def setup_behaviors(portal):
    """Assigns additional behaviors to existing content types
    """
    logger.info("Setup Behaviors ...")
    pt = api.get_tool("portal_types")
    for portal_type, behavior_ids in BEHAVIORS:
        fti = pt.get(portal_type)
        fti_behaviors = fti.behaviors
        additional = filter(lambda b: b not in fti_behaviors, behavior_ids)
        if additional:
            fti_behaviors = list(fti_behaviors)
            fti_behaviors.extend(additional)
            fti.behaviors = tuple(fti_behaviors)

    logger.info("Setup Behaviors [DONE]")


def update_ast_identification(portal):
    """Adds a multiselect interim field to AST's microorganism identification
    service (senaite_ast_identification) to allow the introduction of growth
    number, that is required for "BD EpiCenter"
    https://github.com/beyondessential/pnghealth.lims/issues/170
    """
    logger.info("Update AST identification service ...")
    query = {
        "portal_type": "AnalysisService",
        "getKeyword": IDENTIFICATION_KEY
    }
    brains = api.search(query, SETUP_CATALOG)
    if not brains:
        logger.error("Analysis {} is not present".format(IDENTIFICATION_KEY))
        logger.info("Update AST identification service [SKIP]")
        return

    interim_field = {
        "keyword": "growth",
        "title": "#Growth",
        "value": "",
        "choices": "",
        "result_type": "multivalue",
        "allow_empty": False,
        "unit": "",
        "report": False,
        "hidden": False,
        "wide": False,
        "size": "5",
    }

    service = api.get_object(brains[0])
    service.setInterimFields([interim_field])

    logger.info("Update AST identification service [DONE]")


def fix_default_selective_reporting(portal):
    """Walks through all AST selective reporting analyses and if update their
    interim fields to 'N' if do not have any value set yet
    """
    logger.info("Fixing default result of AST selective reporting tests ...")
    query = {
        "portal_type": "Analysis",
        "getKeyword": REPORT_KEY,
        "review_state": ["assigned", "unassigned", "registered"]
    }
    brains = api.search(query, ANALYSIS_CATALOG)
    for brain in brains:
        analysis = api.get_object(brain)
        # Re-assign interims (the monkey patch takes care of default assignment)
        interim_fields = analysis.getInterimFields()
        analysis.setInterimFields(interim_fields)

    logger.info("Fixing default result of AST selective reporting tests [DONE]")


def rollback_sample(sample_or_uid):
    """Rollback the analyses of the sample from a 'to_be_verified' status to
    the previous status they had before the submit and the sample as well
    """
    wf_id = "senaite_analysis_workflow"
    wf_tool = api.get_tool("portal_workflow")
    workflow = wf_tool.getWorkflowById(wf_id)
    allowed = ["assigned", "unassigned", "registered"]
    sample = api.get_object(sample_or_uid)
    for analysis in sample.getAnalyses(full_objects=True):
        review_history = api.get_review_history(analysis, rev=False)
        review_history = filter(lambda r: r.get("review_state") in allowed, review_history)
        analysis.workflow_history[wf_id] = tuple(review_history)
        workflow.updateRoleMappingsFor(analysis)
        if ISubmitted.providedBy(analysis):
            noLongerProvides(analysis, ISubmitted)
        if IVerified.providedBy(analysis):
            noLongerProvides(analysis, IVerified)

        to_remove = ["to_be_verified", "verified"]
        interim_fields = copy.deepcopy(analysis.getInterimFields())
        for interim in interim_fields:
            for state in to_remove:
                state_id = "status_{}".format(state)
                if state_id in interim:
                    del(interim[state_id])
        analysis.setInterimFields(interim_fields)
        analysis.reindexObject()

    # Try rollback (no remaining analyses or some not submitted)
    doActionFor(sample, "rollback_to_receive")

    logger.info("Fixing default result of AST selective reporting tests [DONE]")


def fix_dismissed_extrapolated_results(portal):
    """Walks through all samples with extrapolated results and updates the value
    for the AST final result test so the selective results for extrapolated
    antibiotics are considered in final result too
    """
    logger.info("Fixing dismissed extrapolated antibiotics in reporting ...")
    query = {
        "portal_type": "Analysis",
        "getKeyword": REPORT_EXTRAPOLATED_KEY
    }
    skip = []
    brains = api.search(query, ANALYSIS_CATALOG)
    for brain in brains:
        analysis = api.get_object(brain)
        sample = analysis.getRequest()
        sample_uid = api.get_uid(sample)
        if sample_uid in skip:
            continue

        skip.append(sample_uid)
        update_sensitivity_result(analysis)

    logger.info("Fixing dismissed extrapolated antibiotics in reporting [DONE]")


def setup_patient_settings(portal):
    """Setup the patient settings by default
    """
    logger.info("Setup default settings for senaite.patient add-on ...")
    for registry_id, value in PATIENT_SETTINGS:
        ploneapi.portal.set_registry_record(registry_id, value)
    logger.info("Setup default settings for senaite.patient add-on [DONE]")


def setup_default_stickers(portal):
    """Sets default stickers to existing sample types
    """
    logger.info("Setup default stickers ...")
    setup = api.get_setup()
    folder = api.get_setup().bika_sampletypes

    # Extract png-specific stickers
    stickers = [sticker["id"] for sticker in getStickerTemplates()]
    stickers = filter(lambda sticker: "palau.lims." in sticker, stickers)

    small_sticker = setup.getSmallStickerTemplate()
    large_sticker = setup.getLargeStickerTemplate()
    for sample_type in folder.objectValues():
        sticker_template = sample_type.getAdmittedStickerTemplates() or [{}]
        sticker_template = sticker_template[0]
        sticker_template["admitted"] = stickers
        if sticker_template.get("small_default") not in stickers:
            sticker_template["small_default"] = small_sticker
        if sticker_template.get("large_default") not in stickers:
            sticker_template["large_default"] = large_sticker
        sample_type.setAdmittedStickerTemplates([sticker_template,])

    logger.info("Setup default stickers [DONE]")


def setup_ast_services_permission(portal):
    """Grant Edit permission for all AST analysis services
    """
    logger.info("Grant edit permission to AST analysis services ...")

    query = {
        "portal_type": "AnalysisService",
        "getKeyword": SERVICES_SETTINGS.keys()
    }

    brains = api.search(query, SETUP_CATALOG)
    for brain in brains:
        service = api.get_object(brain)
        roles = security.get_valid_roles_for(service)
        security.grant_permission_for(service, ModifyPortalContent, roles)

        keyword = service.getKeyword()
        logger.info("Update edit permission for service '{}'".format(keyword))

    logger.info("Grant edit permission to AST analysis services [DONE]")
