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

from bika.lims.api import get_portal
from palau.lims import logger
from palau.lims import PRODUCT_NAME
from palau.lims.setuphandlers import hide_actions
from palau.lims.setuphandlers import setup_behaviors
from palau.lims.setuphandlers import setup_catalogs
from palau.lims.setuphandlers import setup_workflows


def afterUpgradeStepHandler(event):  # noqa CamelCase
    """Event handler executed after running an upgrade step of senaite.core
    """

    logger.info("Run {}.afterUpgradeStepHandler ...".format(PRODUCT_NAME))
    portal = get_portal()
    setup = portal.portal_setup  # noqa

    profile = "profile-{0}:default".format(PRODUCT_NAME)
    setup.runImportStepFromProfile(profile, "actions")
    setup.runImportStepFromProfile(profile, "typeinfo")
    setup.runImportStepFromProfile(profile, "rolemap")
    setup.runImportStepFromProfile(profile, "workflow")

    # Setup catalogs
    setup_catalogs(portal)

    # Add behaviors
    setup_behaviors(portal)

    # Setup workflows
    setup_workflows(portal)

    # Hide actions from both navigation portlet and from control_panel
    hide_actions(portal)

    logger.info("Run {}.afterUpgradeStepHandler [DONE]".format(PRODUCT_NAME))
