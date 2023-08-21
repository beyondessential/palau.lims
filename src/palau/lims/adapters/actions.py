# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from bika.lims.browser.workflow import RequestContextAware
from bika.lims.interfaces import IWorkflowActionUIDsAdapter
from palau.lims import messageFactory as _
from zope.interface import implementer


@implementer(IWorkflowActionUIDsAdapter)
class CreateSupplementaryAdapter(RequestContextAware):
    """Adapter that handles "create_supplementary" action. Redirects the user
    the the Add Sample form, but with Primary field visible and with the
    samples for which the transition was triggered selected
    """

    def __call__(self, action, uids):
        """Redirect the user to the Add form
        """
        if len(uids) > 4:
            return self.redirect(message=_("Too many samples selected"),
                                 level="error")

        container = self.get_add_container()
        uids_str = ",".join(uids)
        url = "{}/ar_add?ar_count={}&primary={}&copy_from={}".format(
            api.get_url(container), len(uids),  uids_str, uids_str)
        return self.redirect(redirect_url=url)

    def get_add_container(self):
        """Returns the container from which the ar_add endpoint has to be called
        """
        client = api.get_current_client()
        if client:
            return client
        return api.get_portal().samples
