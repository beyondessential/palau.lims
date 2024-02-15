# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd


from palau.lims import utils
from senaite.ast.browser.addpanel import AddPanelView as BaseView


class AddPanelView(BaseView):

    def __call__(self):
        # set the panel to current sample
        panel_uid = self.request.form.get("panel_uid")
        utils.set_ast_panel_to_sample(panel_uid, self.context)

        # return response from base class
        return super(AddPanelView, self).__call__()
