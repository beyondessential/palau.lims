# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS.
#
# PALAU.LIMS is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2023-2025 by it's authors.
# Some rights reserved, see README and LICENSE.

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
