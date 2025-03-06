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

import copy
from datetime import datetime

from bika.lims import api
from bika.lims.browser import BrowserView
from bika.lims.utils import createPdf
from bika.lims.utils import get_client
from plone.memoize import view
from palau.lims.utils import get_field_value
from palau.lims.utils import get_fullname
from palau.lims.utils import to_localized_time
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from senaite.app.supermodel import SuperModel
from senaite.patient.api import get_age_ymd
from senaite.patient.config import SEXES
from slugify import slugify
from weasyprint.compat import base64_encode


class RejectionView(BrowserView):
    """View of the Sample rejection report
    """
    template = ViewPageTemplateFile("templates/rejection.pt")
    content = ViewPageTemplateFile("templates/rejection_content.pt")

    def __call__(self):
        return self.template()

    @property
    def sample(self):
        """Returns a SuperModel of the current Sample
        """
        return SuperModel(self.context)

    @property
    def client(self):
        """Returns a SuperModel of the client the current Sample belongs to
        """
        client = get_client(self.context)
        return SuperModel(client)

    @property
    def laboratory(self):
        """Returns a supermodel of the LIMS's laboratory object
        """
        laboratory = api.get_setup().laboratory
        return SuperModel(laboratory)

    @property
    def document_date(self):
        """Returns the date of the document
        """
        return datetime.now()

    def localize(self, date, **kw):
        """Converts the given date to a localized time string
        """
        return to_localized_time(date, **kw)

    def get_image_url(self, file_name):
        portal = api.get_portal()
        base_url = api.get_url(portal)
        url = "{}/++plone++palau.lims.static/assets/images/{}"
        return url.format(base_url, file_name)

    def get_client_logo_src(self, client):
        """Returns the src suitable for embedding into img html element of the
        client's logo, if any. Returns None otherwise
        """
        logo = client.getReportLogo()
        if not logo:
            return None
        return self.get_image_blob_src(logo)

    def get_lab_logo_src(self):
        """Returns the src suitable for embedding into img html element of the
        laboratory's logo, if any. Returns None otherwise
        """
        setup = api.get_setup()
        logo = setup.getReportLogo()
        return self.get_image_blob_src(logo)

    def get_image_blob_src(self, img):
        """Returns the src suitable for embedding into html element
        """
        if not img:
            return None
        data_url = "data:"+img.content_type+";base64," + (
            base64_encode(img.data).decode("ascii").replace("\n", ""))
        return data_url

    def get_age(self, dob, onset_date=None):
        """Returns a string that represents the age in ymd format
        """
        return get_age_ymd(dob, onset_date) or ""

    def get_dob(self, sample):
        """Returns the Date of birth (datetime) assigned to the patient of
        the sample. Returns None if no dob is set
        """
        return sample.getDateOfBirth()[0]

    def get_sex(self, sample):
        """Returns the sex (text) assigned to the sample
        """
        sample = api.get_object(sample)
        sex = sample.getSex()
        sex = dict(SEXES).get(sex, "")
        return sex.encode("utf-8")

    def get_laboratory_reasons(self):
        """Returns the list of predefined reasons of rejection, following the
        same order as defined in Setup
        """
        setup = api.get_setup()
        return setup.getRejectionReasonsItems()

    def get_sample_reasons(self):
        """Returns the list of rejection reasons from the sample
        """
        reasons = self.context.getRejectionReasons()
        reasons = reasons and reasons[0] or {}
        return reasons.get("selected", [])

    def get_reasons(self):
        """Return a list made of tuples of (True/False, 'reason text') with
        all the predefined reasons from the laboratory plus those from the
        sample
        """
        reasons = self.get_laboratory_reasons()
        sample_reasons = self.get_sample_reasons()

        # Add reasons from sample (maybe the sample was rejected before the
        # current rejection reasons were set) if not there
        for sample_reason in sample_reasons:
            if sample_reason not in reasons:
                reasons.append(sample_reason)

        return [(reason in sample_reasons, reason) for reason in reasons]

    def get_other_reasons(self):
        """Returns the text for user-custom reasons of rejection
        """
        reasons = self.context.getRejectionReasons()
        reasons = reasons and reasons[0] or {}
        return reasons.get("other", "")

    def get_date_rejected(self):
        """Returns the transition date from the Analysis Request object
        """
        rejection_info = self.get_rejection_info()
        return rejection_info.get("time")

    def get_rejected_by(self):
        """Returns the user reject
        """
        rejection_info = self.get_rejection_info()
        actor = rejection_info.get("actor")
        return get_fullname(actor) or ""

    @view.memoize
    def get_rejection_info(self):
        """Returns the info about the last rejection transition
        """
        review_history = api.get_review_history(self.context)
        for event in review_history:
            if event.get("action") == "reject":
                # do a hard copy of value (this is a mutable type)
                return copy.deepcopy(event)
        return {}


class RejectionPdfView(RejectionView):
    """Print view w/o outer contents of the Sample rejection report
    """
    template = ViewPageTemplateFile("templates/rejection_print.pt")

    def __call__(self):
        pdf = self.create_pdf()
        parts = [
            "rejection",
            api.get_id(self.context),
            self.document_date.strftime("%Y%m%d"),
        ]
        parts = [slugify(prt, separator="-", lowercase=False) for prt in parts]
        parts = "_".join(parts)
        filename = "{}.pdf".format(parts)
        return self.download(pdf, filename)

    def site_url(self):
        """Returns the site url
        """
        return api.get_url(api.get_portal())

    def create_pdf(self):
        """Creates a PDF of the rejection report
        """
        html_data = self.template()
        html_data = safe_unicode(html_data).encode("utf-8")
        return createPdf(html_data)

    def download(self, data, filename, content_type="application/pdf"):
        """Downloads the PDF of the rejection report
        """
        self.request.response.setHeader(
            "Content-Disposition", "attachment; filename=%s" % filename)
        self.request.response.setHeader("Content-Type", content_type)
        self.request.response.setHeader("Content-Length", len(data))
        self.request.response.setHeader("Cache-Control", "no-store")
        self.request.response.setHeader("Pragma", "no-cache")
        self.request.response.write(data)
