# -*- coding: utf-8 -*-

import transaction
from bika.lims import api
from palau.lims import logger
from palau.lims.scripts import setup_script_environment
from senaite.core.catalog import SAMPLE_CATALOG
from senaite.core.upgrade.utils import delete_object


def assigned_to_worksheets(sample):
    """Returns a list with the worksheets this sample is assigned to
    """
    brains = sample.getAnalyses()
    for brain in brains:
        analysis = api.get_object(brain)
        if analysis.getWorksheetUID():
            return True
    return False


def main(app):
    # Setup environment
    setup_script_environment(app)

    query = {
        "portal_type": "AnalysisRequest",
        "review_state": "dispatched",
    }

    brains = api.search(query, SAMPLE_CATALOG)
    total = len(brains)
    for num, brain in enumerate(brains):
        if num > 0 and num % 100 == 0:
            logger.info("Removing dispatched samples: %s/%s" % (num, total))

        sample = api.get_object(brain)
        sid = api.get_id(sample)

        # is assigned to a worksheet?
        if assigned_to_worksheets(sample):
            logger.warn("[SKIP] Sample %s is assigned to a Worksheet" % sid)
            sample._p_deactivate()
            continue

        # delete the sample
        delete_object(sample)

    # Commit transaction
    logger.info("Commit transaction ...")
    transaction.commit()
    logger.info("Commit transaction [DONE]")


if __name__ == "__main__":
    main(app)  # noqa: F821
