# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from bika.lims.interfaces import IVerified
from palau.lims import logger
from palau.lims import PRODUCT_NAME as product
from palau.lims.setuphandlers import setup_behaviors
from palau.lims.setuphandlers import setup_catalogs
from palau.lims.setuphandlers import setup_roles_and_groups
from palau.lims.setuphandlers import setup_workflows
from palau.lims.workflow.analysis.events import after_set_out_of_stock
from senaite.core.catalog import ANALYSIS_CATALOG
from senaite.core.catalog import SAMPLE_CATALOG
from senaite.core.upgrade import upgradestep
from senaite.core.upgrade.utils import uncatalog_brain
from senaite.core.upgrade.utils import UpgradeUtils
from senaite.core.workflow import ANALYSIS_WORKFLOW

version = "1.0.0"  # Remember version number in metadata.xml and setup.py
profile = "profile-{0}:default".format(product)


@upgradestep(product, version)
def upgrade(tool):
    portal = tool.aq_inner.aq_parent
    ut = UpgradeUtils(portal)
    ver_from = ut.getInstalledVersion(product)

    if ut.isOlderVersion(product, version):
        logger.info("Skipping upgrade of {0}: {1} > {2}".format(
            product, ver_from, version))
        return True

    logger.info("Upgrading {0}: {1} -> {2}".format(product, ver_from, version))

    # -------- ADD YOUR STUFF BELOW --------

    logger.info("{0} upgraded to version {1}".format(product, version))
    return True


def set_site_from_samplepoint(tool):
    """Re-assigns the value of Site field with the existing value of
    SamplePoint
    """
    query = {"portal_type": "AnalysisRequest"}
    brains = api.search(query, SAMPLE_CATALOG)
    total = len(brains)

    for num, brain in enumerate(brains):
        if num and num % 100 == 0:
            logger.info("Update Site value {0}/{1}".format(num, total))

        obj = api.get_object(brain, default=None)
        if not obj:
            uncatalog_brain(brain)
            continue

        site = obj.getSite()
        if site:
            continue

        sample_point = obj.getRawSamplePoint()
        if not api.is_uid(sample_point):
            sample_point = None
        obj.setSite(sample_point)
        obj.reindexObject()


def add_patient_behavior(tool):
    """Add patient behavior
    """
    logger.info("Add Patient behavior ...")
    portal = api.get_portal()
    setup_behaviors(portal)
    logger.info("Add Patient behavior [DONE]")


def setup_statistic_reports(tool):
    """Adds the statistic reports portal action
    """
    logger.info("Setup statistic reports ...")
    portal = tool.aq_inner.aq_parent
    setup = portal.portal_setup
    setup.runImportStepFromProfile(profile, "actions")
    logger.info("Setup statistic reports [DONE]")


def setup_analysis_by_department_report(tool):
    """Setup the catalog indexes/metadata required for the analysis by
    department to work properly and reindex all analyses for the changes
    to take effect to existing objects.
    """
    portal = tool.aq_inner.aq_parent
    setup_catalogs(portal)

    # re-catalog metadata analysis objects
    logger.info("Updating metadata of analysis objects ...")
    cat = api.get_tool(ANALYSIS_CATALOG)
    uc = api.get_tool("uid_catalog")
    brains = uc(portal_type="Analysis")
    total = len(brains)
    for num, brain in enumerate(brains):
        if num and num % 100 == 0:
            logger.info("Processed objects: {0}/{1}".format(num, total))

        obj = api.get_object(brain, default=None)
        if not obj:
            uncatalog_brain(brain)
            continue

        # Update metadata for the given catalog and object
        obj = api.get_object(obj)
        obj_url = api.get_path(obj)
        cat.catalog_object(obj, obj_url, idxs=(), update_metadata=1)

        # Flush the object from memory
        obj._p_deactivate()

    logger.info("Updating metadata of analysis objects ...")


def setup_analysis_workflow(tool):
    """Adds the analysis workflow portal action
    and updates the analyses states and transitions
    """
    logger.info("Setup analysis workflow ...")

    #  Update Analyses workflow
    portal = tool.aq_inner.aq_parent
    setup = portal.portal_setup
    setup.runImportStepFromProfile(profile, "rolemap")
    setup_workflows(api.get_portal())

    # Update Analyses rolemap
    statuses = ["assigned", "unassigned"]
    query = {"portal_type": "Analysis", "review_state": statuses}
    brains = api.search(query, ANALYSIS_CATALOG)

    wf_tool = api.get_tool("portal_workflow")
    wf = wf_tool.getWorkflowById(ANALYSIS_WORKFLOW)

    for brain in brains:
        obj = api.get_object(brain)
        wf.updateRoleMappingsFor(obj)

        # Flush the object from memory
        obj._p_deactivate()

    logger.info("Setup analysis workflow [DONE]")


def fix_out_of_stock(tool):
    """Walks through all analyses in out-of-stock status and sets the result
    to Out of stock
    """
    query = {"portal_type": "Analysis", "review_state": "out_of_stock"}
    brains = api.search(query, ANALYSIS_CATALOG)
    for brain in brains:
        obj = api.get_object(brain)
        if IVerified.providedBy(obj):
            continue

        # Mark the analysis as out-of-stock and tries to submit the sample
        after_set_out_of_stock(obj)

        # Flush the object from memory
        obj._p_deactivate()

    logger.info("Setup analysis workflow [DONE]")


def setup_rejector(tool):
    portal = tool.aq_inner.aq_parent
    setup = portal.portal_setup

    logger.info("Setting Rejector role for Analyses [BEGIN]...")

    setup.runImportStepFromProfile(profile, "rolemap")
    setup_roles_and_groups(portal)

    # Update Analyses rolemap
    states = ["assigned", "unassigned", "to_be_verified"]
    query = {"portal_type": "Analysis", "review_state": states}
    brains = api.search(query, ANALYSIS_CATALOG)

    wf_tool = api.get_tool("portal_workflow")
    wf = wf_tool.getWorkflowById(ANALYSIS_WORKFLOW)

    for brain in brains:
        obj = api.get_object(brain)
        wf.updateRoleMappingsFor(obj)

        # Flush the object from memory
        obj._p_deactivate()

    logger.info("Rejector role set successfully for Analyses [END]...")
    return True
