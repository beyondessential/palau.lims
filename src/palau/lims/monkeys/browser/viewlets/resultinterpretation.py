# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import copy
from plone import protect
from Products.Archetypes.event import ObjectEditedEvent
from zope import event
from bika.lims import api
from bika.lims import logger
from bika.lims import senaiteMessageFactory as _


def handle_form_submit(self):
    """Handle form submission of Result Interpretation
    """
    protect.CheckAuthenticator(self.request)
    logger.info("Handle ResultsInterpration Submit")
    # Save the results interpretation
    res = self.request.form.get("ResultsInterpretationDepts", [])

    # Get the current user when submitted
    current_user = api.get_current_user()
    user = current_user.getProperty('id')

    # Pass res and user as argument
    res_user = (res, user)
    self.context.setResultsInterpretationDepts(res_user)

    self.add_status_message(_("Changes Saved"), level="info")
    # reindex the object after save to update all catalog metadata
    self.context.reindexObject()
    # notify object edited event
    event.notify(ObjectEditedEvent(self.context))
    return self.request.response.redirect(api.get_url(self.context))


def get_resultsinterpretation(self):
    ri_by_depts = self.ResultsInterpretationDepts
    logger.info(ri_by_depts)

    out = []
    for ri in ri_by_depts:
        dept = ri.get("uid", "")
        title = getattr(dept, "title", "")
        richtext = ri.get("richtext", "")
        user = ri.get("user", "")
        out.append({"title": title, "richtext": richtext, "user": user})

    return out
