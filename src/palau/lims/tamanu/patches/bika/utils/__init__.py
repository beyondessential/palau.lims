# -*- coding: utf-8 -*-

from bika.lims.utils import analysisrequest as _analysisrequest
from .analysisrequest import do_rejection

# https://pypi.org/project/collective.monkeypatcher/#patching-module-level-functions
_analysisrequest.do_rejection = do_rejection
