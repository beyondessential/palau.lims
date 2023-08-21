# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims.browser.stickers import Sticker
from palau.lims import utils


class StickersDefaultView(Sticker):
    """Product-specific controller view for stickers/labels
    """

    def long_date(self, date):
        """Returns the localized date in long format
        """
        return utils.to_localized_time(date, long_format=1)

    def short_date(self, date):
        """Returns the localized date in short format
        """
        return utils.to_localized_time(date, long_format=0)
