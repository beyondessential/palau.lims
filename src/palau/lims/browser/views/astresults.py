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

from collections import OrderedDict
from bika.lims import api
from plone.memoize import view
from palau.lims.utils import is_growth_editable
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from senaite.ast.browser.results import ManageResultsView
from senaite.ast.config import RESISTANCE_KEY
from senaite.ast.utils import get_ast_analyses
from senaite.ast.utils import get_microorganisms


class ManageASTResultsView(ManageResultsView):
    """Listing view for AST results entry
    """
    contents_table_template = ViewPageTemplateFile("templates/ast_results.pt")

    def update(self):
        """Update hook
        """
        # Add GrowthNumber column
        new_columns = (
            ("GrowthNumber", {
                "title": "#Growth",
                "sortable": False,
                "input_width": "2",
                "toggle": True,
                "ajax": True,
            }),
        )
        old_columns = self.columns.items()
        self.columns = OrderedDict(list(new_columns) + list(old_columns))

        # Remove the columns we are not interested in from review_states
        hide = ["Method", "Instrument", "Analyst", "DetectionLimitOperand",
                "Specification", "Uncertainty", "retested", "Attachments",
                "DueDate", "Result", "Hidden", "Unit"]
        all_columns = self.columns.keys()
        all_columns = filter(lambda c: c not in hide, all_columns)
        for review_state in self.review_states:
            review_state.update({"columns": all_columns})

        # Delegate to super class' update
        super(ManageASTResultsView, self).update()

    def folderitem(self, obj, item, index):
        super(ManageASTResultsView, self).folderitem(obj, item, index)

        # Render the growth number field
        obj = self.get_object(obj)
        item["GrowthNumber"] = obj.getGrowthNumber()

        # editable if at least one of the AST siblings is not yet verified
        if is_growth_editable(obj):
            item.setdefault("allow_edit", []).append("GrowthNumber")

        return item

    def folderitems(self):
        items = super(ManageASTResultsView, self).folderitems()

        # Apply rowspan for GrowthNumber
        for item in items:
            rowspan = item.get("rowspan", {})
            microspan = rowspan.get("Microorganism")
            if microspan:
                item["rowspan"]["GrowthNumber"] = microspan

            skip = item.get("skip", [])
            if "Microorganism" in skip:
                skip.append("GrowthNumber")
                item["skip"] = skip

        return items

    def get_panel_info(self, brain_or_object):
        panel_info = super(ManageASTResultsView, self).get_panel_info(
            brain_or_object
        )
        panel_info["description"] = api.get_description(brain_or_object)

        # Get the microorganisms assigned to this sample
        existing = self.get_sensitivity_microorganisms(self.context)

        # Get the microorganisms assigned to this panel
        panel = api.get_object(brain_or_object)
        assigned = [api.get_object(obj) for obj in panel.microorganisms]

        # Find microorganisms from panel that are missing in the sample
        missing = set(existing) - set(assigned)

        # Assign the names of the missing microorganisms
        missing = [api.get_title(obj) for obj in missing]
        panel_info["missing_microorganisms"] = ", ".join(sorted(missing))

        return panel_info

    def get_sensitivity_microorganisms(self, sample):
        analyses = get_ast_analyses(sample)
        sensitivity = filter(
            lambda s: s.getKeyword() == RESISTANCE_KEY, analyses
        )
        return get_microorganisms(sensitivity)

    @view.memoize
    def get_context_panels_info(self):
        self.context.panels = getattr(self.context, "panels", []) or []
        panels = map(api.get_object, self.context.panels)
        return map(self.get_panel_info, panels)

    def is_panels_info_visible(self):
        panels = getattr(self.context, "panels", []) or []
        if panels:
            return True
        return False
