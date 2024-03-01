# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import os

from bika.lims import api
from bika.lims.api import security
from bika.lims.browser.analysisrequest.add2 import AR_CONFIGURATION_STORAGE
from BTrees.OOBTree import OOBTree
from palau.lims import logger
from palau.lims import permissions
from palau.lims import PRODUCT_NAME
from palau.lims import PROFILE_ID
from palau.lims.config import ACTIONS_TO_HIDE
from palau.lims.config import ID_FORMATTING
from palau.lims.config import IMPRESS_SETTINGS
from palau.lims.config import LABORATORY_SETTINGS
from palau.lims.config import LANG_SETTINGS
from palau.lims.config import PATIENT_SETTINGS
from palau.lims.config import REJECTION_REASONS
from palau.lims.config import SAMPLE_ADD_FIELDS_TO_HIDE
from palau.lims.config import SAMPLE_FIELDS_ORDER
from palau.lims.config import SETUP_SETTINGS
from plone import api as ploneapi
from plone.registry.interfaces import IRegistry
from Products.DCWorkflow.Guard import Guard
from senaite.abx.interfaces import IAntibiotic
from senaite.abx.interfaces import IAntibioticClass
from senaite.ast.config import AST_CALCULATION_TITLE
from senaite.ast.config import IDENTIFICATION_KEY
from senaite.ast.config import SERVICE_CATEGORY
from senaite.ast.config import SERVICES_SETTINGS
from senaite.core import permissions as permissionsCore
from senaite.core.catalog import ANALYSIS_CATALOG
from senaite.core.catalog import SAMPLE_CATALOG
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.permissions import FieldEditRemarks
from senaite.core.setuphandlers import setup_core_catalogs
from senaite.core.setuphandlers import setup_other_catalogs
from senaite.core.upgrade.utils import delete_object
from senaite.core.workflow import ANALYSIS_WORKFLOW
from senaite.core.workflow import SAMPLE_WORKFLOW
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility

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
    (ANALYSIS_CATALOG, "getDepartmentTitle"),
]

# Skin layers that have priority over others, sorted from more to less priority
SORTED_SKIN_LAYERS = [
    "custom",
    "palau.lims",
    "bika",
]

# Tuples of ID, Title, FTI
SETUP_FOLDERS = [
    ("wards", "Wards", "Wards"),
    ("warddepartments", "Ward Departments", "WardDepartments"),
]

# Tuples of (portal_type, list of behaviors)
BEHAVIORS = [
    ("SampleContainer", [
        "palau.lims.behaviors.samplecontainer.IExtendedSampleContainerBehavior",  # noqa
    ]),
    ("Patient", [
        "palau.lims.behaviors.patient.IExtendedPatientBehavior"
    ]),
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
                    "guard_permissions": permissions.TransitionCreateSupplementary,  # noqa
                    "guard_roles": "",
                    "guard_expr": "python:here.guard_handler('create_supplementary')",  # noqa
                }
            }
        }
    },
    ANALYSIS_WORKFLOW: {
        "states": {
            "assigned": {
                "preserve_transitions": True,
                "transitions": ("set_out_of_stock",),
            },
            "unassigned": {
                "preserve_transitions": True,
                "transitions": ("set_out_of_stock",),
            },
            "out_of_stock": {
                "title": "Out of Stock",
                "permissions_copy_from": "rejected",
            },
        },
        "transitions": {
            "set_out_of_stock": {
                "title": "Set Out of Stock",
                "new_state": "out_of_stock",
                "action": "Set Out of Stock",
                "guard": {
                    "guard_permissions": permissions.TransitionSetOutOfStock,
                    "guard_roles": "",
                    "guard_expr":
                        "python:here.guard_handler('set_out_of_stock')",
                }
            }
        }
    },
}


# List of tuples of (role, path, [(permissions, acquire), ...])
# When path is empty/None, the permissions are applied to portal object
ROLES = [
    ("Rejector", "", [
        (permissionsCore.TransitionRejectAnalysis, 0),
    ]),
]

# List of tuples of (id, title, roles)
GROUPS = [
    ("Rejectors", "Rejectors", [
        "Member", "Rejector", "Analyst"
    ]),
]


def setup_handler(context):
    """Generic setup handler
    """
    if context.readDataFile('palau.lims.txt') is None:
        return

    logger.info("{} setup handler [BEGIN]".format(PRODUCT_NAME.upper()))
    portal = context.getSite()

    # Setup the sorting of skin layers
    setup_skin_layers(portal)

    # Setup catalogs
    setup_catalogs(portal)

    # Setup roles and groups
    setup_roles_and_groups(portal)

    # Setup folders
    add_setup_folders(portal)

    # Add behaviors
    setup_behaviors(portal)

    # Setup workflows
    setup_workflows(portal)

    # Import baseline data
    import_content_structure(portal)

    # Configure visible navigation items
    setup_navigation_types(portal)

    # Setup languages
    setup_languages(portal)

    # Setup laboratory information
    setup_laboratory(portal)

    # Setup default settings
    setup_default_settings(portal)

    # Apply ID format to content types
    setup_id_formatting(portal)

    # setup rejection reasons
    setup_rejection_reasons(portal)

    # Apply impress default settings
    setup_impress_settings(portal)

    # Apply patient default settings
    setup_patient_settings(portal)

    # Sort fields from Add Sample form
    setup_sample_add_fields(portal)

    # Hide actions from both navigation portlet and from control_panel
    hide_actions(portal)

    # Add multiselect interim for AST's Microorganism identification to allow
    # the introduction of growth number required for "BD EpiCenter"
    # https://github.com/beyondessential/pnghealth.lims/issues/170
    update_ast_identification(portal)

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


def import_content_structure(portal):
    logger.info("Importing content structure ...")

    # Delete pre-existing objects we do not want to re-import
    delete_ast_objects(portal)
    delete_antibiotics(portal)
    delete_antibiotics_classes(portal)

    # Get the tarball full path
    src_path = "/src/{}".format(PRODUCT_NAME.replace(".", "/"))
    dirname = os.path.dirname(os.path.abspath(__file__))
    dirname = dirname.replace(src_path, "")
    tarball = "{}/structure.tar.gz".format(dirname)

    # Import the tarball
    portal_setup = api.get_tool("portal_setup")
    logger.info("Importing {} ...".format(tarball))
    tarball_file = open(tarball, mode="r")
    portal_setup.manage_importTarball(tarball_file)
    logger.info("Importing content structure [DONE]")


def delete_antibiotics_classes(portal):
    """Removes existing antibiotic classes
    """
    logger.info("Deleting antibiotic classes ...")
    folder = api.get_setup().get("antibiotic_classes")
    for obj in folder.objectValues():
        if not IAntibioticClass.providedBy(obj):
            continue
        obj_id = api.get_id(obj)
        obj_path = api.get_path(obj)
        logger.info("Deleting {} ({})".format(obj_path, obj_id))
        delete_object(obj)
    logger.info("Deleting antibiotic classes [DONE]")


def delete_antibiotics(portal):
    """Removes existing antibiotics
    """
    logger.info("Deleting antibiotics ...")
    folder = api.get_setup().get("antibiotics")
    for obj in folder.objectValues():
        if not IAntibiotic.providedBy(obj):
            continue
        obj_id = api.get_id(obj)
        obj_path = api.get_path(obj)
        logger.info("Deleting {} ({})".format(obj_path, obj_id))
        delete_object(obj)
    logger.info("Deleting antibiotics [DONE]")


def delete_ast_objects(portal):
    """Remove auto-generated objects from senaite.ast
    """
    # AST Services
    query = {"portal_type": "AnalysisService",
             "getKeyword": SERVICES_SETTINGS.keys()}
    brains = api.search(query, SETUP_CATALOG)
    to_remove = map(api.get_object, brains)

    # AST Category and Calculation
    query = {"portal_type": ["AnalysisCategory", "Calculation"],
             "title": [SERVICE_CATEGORY, AST_CALCULATION_TITLE]}
    brains = api.search(query, SETUP_CATALOG)
    to_remove.extend(map(api.get_object, brains))

    for obj in to_remove:
        delete_object(obj)


def setup_skin_layers(portal):
    """Setup the sorting of skin layers
    """
    logger.info("Setup Skin layers ...")
    skins_tool = api.get_tool("portal_skins")
    selections = skins_tool._getSelections()

    # For each skin, resort the skins layers in accordande
    for skin_name in selections.keys():
        layers = selections[skin_name].split(",")
        filtered = filter(lambda lay: lay not in SORTED_SKIN_LAYERS, layers)
        new_layers = SORTED_SKIN_LAYERS + filtered
        selections[skin_name] = ",".join(new_layers)

    logger.info("Setup Skin layers [DONE]")


def setup_default_settings(portal):
    """Setup the settings by default
    """
    logger.info("Setup default settings ...")
    setup = api.get_setup()
    api.edit(setup, check_permissions=False, **dict(SETUP_SETTINGS))
    logger.info("Setup default settings [DONE]")


def setup_laboratory(portal):
    """Setup Laboratory
    """
    logger.info("Setup Laboratory ...")
    setup = api.get_setup()
    lab = setup.laboratory
    api.edit(lab, check_permissions=False, **dict(LABORATORY_SETTINGS))
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


def set_nav_visibility(obj, visible):
    """Sets the visibility of the object in the navigation bar
    """
    if hasattr(obj, "setExpirationDate"):
        obj.setExpirationDate(None)

    if api.is_dexterity_content(obj):
        obj.exclude_from_nav = visible
    else:
        obj.setExcludeFromNav(visible)
    obj.reindexObject()


def hide_action(folder, action_id):
    logger.info("Hiding {} from {} ...".format(action_id, folder.id))
    if action_id not in folder:
        logger.info("{} not found in {} [SKIP]".format(action_id, folder.id))
        return

    item = folder[action_id]
    logger.info("Hide {} ({}) from nav bar".format(action_id, item.Title()))
    set_nav_visibility(item, False)

    def get_action_index(action_id):
        for n, action in enumerate(cp.listActions()):
            if action.getId() == action_id:
                return n
        return -1

    logger.info("Hide {} from control_panel".format(action_id, item.Title()))  # noqa
    cp = api.get_tool("portal_controlpanel")
    action_index = get_action_index(action_id)
    if action_index == -1:
        logger.info("{}  not found in control_panel [SKIP]".format(cp.id))
        return

    actions = cp._cloneActions()  # noqa
    del actions[action_index]
    cp._actions = tuple(actions)
    cp._p_changed = 1


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


def setup_sample_add_fields(portal):
    logger.info("Setup Sample Add fields ...")

    ordered_fields = SAMPLE_FIELDS_ORDER
    to_hide = SAMPLE_ADD_FIELDS_TO_HIDE

    # Sort fields
    storage = get_manage_add_storage(portal)
    storage.update({"order": ordered_fields})
    update_manage_add_storage(portal, storage)

    # Hide fields
    storage = get_manage_add_storage(portal)
    visibility = storage.get('visibility', {}).copy()
    fields = list(set(visibility.keys() + to_hide + ordered_fields))
    for field_name in fields:
        visibility[field_name] = field_name not in to_hide
    storage.update({"visibility": visibility})
    update_manage_add_storage(portal, storage)
    logger.info("Setup Sample Add fields [DONE]")


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
    new_status.description = settings.get(
        "description", new_status.description
    )

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


def setup_impress_settings(portal):
    """Setup impress
    """
    logger.info("Setup Impress settings ...")
    for key, value in IMPRESS_SETTINGS:
        registry_id = "senaite.impress.{}".format(key)
        ploneapi.portal.set_registry_record(registry_id, value)
    logger.info("Setup Impress settings [DONE]")


def setup_behaviors(portal):
    """Assigns additional behaviors to existing content types
    """
    logger.info("Setup Behaviors ...")
    pt = api.get_tool("portal_types")
    for portal_type, behavior_ids in BEHAVIORS:
        fti = pt.get(portal_type)
        if not hasattr(fti, "behaviors"):
            continue
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


def setup_patient_settings(portal):
    """Setup the patient settings by default
    """
    logger.info("Setup default settings for senaite.patient add-on ...")
    for registry_id, value in PATIENT_SETTINGS:
        ploneapi.portal.set_registry_record(registry_id, value)
    logger.info("Setup default settings for senaite.patient add-on [DONE]")


def setup_rejection_reasons(portal):
    """Enables the rejection workflow and sets the rejection reasons
    """
    logger.info("Enabling the rejection workflow ...")
    setup = api.get_setup()
    reasons_dict = {"checkbox": "on"}
    for number, reason in enumerate(REJECTION_REASONS):
        r_text_key = "textfield-{}".format(number)
        r_text_value = reason
        reasons_dict[r_text_key] = r_text_value
    setup.setRejectionReasons(reasons_dict)
    logger.info("Enabling the rejection workflow [DONE]")


def setup_languages(portal):
    """Setup the default settings re languages
    """
    logger.info("Setup languages settings ...")
    for key, val in LANG_SETTINGS:
        ploneapi.portal.set_registry_record("plone.{}".format(key), val)
    logger.info("Setup languages settings [DONE]")


def setup_roles(portal):
    """Setup roles
    """
    logger.info("Setup roles ...")
    for role, path, perms in ROLES:
        folder_path = path or api.get_path(portal)
        folder = api.get_object_by_path(folder_path)
        for permission, acquire in perms:
            logger.info("{} {} {} (acquire={})".format(role, folder_path,
                                                       permission, acquire))
            security.grant_permission_for(folder, permission, role,
                                          acquire=acquire)
    logger.info("Setup roles [DONE]")


def setup_groups(portal):
    """Setup roles and groups
    """
    logger.info("Setup groups ...")
    portal_groups = api.get_tool("portal_groups")
    for group_id, title, roles in GROUPS:

        # create the group and grant the roles
        if group_id not in portal_groups.listGroupIds():
            logger.info("Adding group {} ({}): {}".format(
                title, group_id, ", ".join(roles)))
            portal_groups.addGroup(group_id, title=title, roles=roles)

        # grant the roles to the existing group
        else:
            ploneapi.group.grant_roles(groupname=group_id, roles=roles)
            logger.info("Granting roles for group {} ({}): {}".format(
                title, group_id, ", ".join(roles)))

    logger.info("Setup groups [DONE]")


def setup_roles_and_groups(portal):
    """Setup roles and groups
    """
    setup_roles(portal)
    setup_groups(portal)
