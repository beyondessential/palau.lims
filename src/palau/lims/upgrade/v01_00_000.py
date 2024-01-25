# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from palau.lims import logger
from palau.lims import PRODUCT_NAME as product
from palau.lims.setuphandlers import setup_behaviors
from palau.lims.setuphandlers import setup_workflows
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
    portal = api.get_portal()

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

def setup_analysis_workflow(tool):
    """Adds the analysis workflow portal action
    and updates the analyses states and transitions
    """
    logger.info("Setup analysis workflow ...")

    #  Update Analyses workflow
    setup.runImportStepFromProfile(profile, "rolemap")
    setup_workflows(api.get_portal())

    # Update Analyses rolemap
    query = {"portal_type": "Analysis", "review_state": ["assigned", "unassigned"]}
    brains = api.search(query, ANALYSIS_CATALOG)

    wf_tool = api.get_tool("portal_workflow")
    wf = wf_tool.getWorkflowById(ANALYSIS_WORKFLOW)

    for brain in brains:
        obj = api.get_object(brain)
        wf.updateRoleMappingsFor(obj)

    logger.info("Setup analysis workflow [DONE]")
