# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import transaction
from palau.lims import logger
from bika.lims import api
from senaite.impress.decorators import synchronized
from senaite.impress.storage import PdfReportStorageAdapter as BaseAdapter
from bika.lims.workflow import doActionFor as do_action_for


class PdfReportStorageAdapter(BaseAdapter):
    """Storage adapter for PDF reports
    """

    @synchronized(max_connections=1)
    def create_report(self, parent, pdf, html, uids, metadata):
        """Create a new report object

        NOTE: We limit the creation of reports to 1 to avoid conflict errors on
              simultaneous publication.

        :param parent: parent object where to create the report inside
        :returns: ARReport
        """

        parent_id = api.get_id(parent)
        logger.info("Create Report for {} ...".format(parent_id))

        # Manually update the view on the database to avoid conflict errors
        parent._p_jar.sync()

        # Create the report object
        report = api.create(
            parent,
            "ARReport",
            AnalysisRequest=api.get_uid(parent),
            Pdf=pdf,
            Html=html,
            ContainedAnalysisRequests=uids,
            Metadata=metadata)

        # Transition the sample to published status
        do_action_for(parent, "publish")

        # Commit the changes
        transaction.commit()

        logger.info("Create Report for {} [DONE]".format(parent_id))

        return report
