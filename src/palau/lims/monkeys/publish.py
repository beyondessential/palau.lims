# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd
import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _BMF
from bika.lims import senaiteMessageFactory as _
from bika.lims.utils import get_link
from bika.lims.browser.publish.reports_listing import ReportsListingView
from Products.CMFPlone.utils import safe_unicode
from senaite.core.catalog import REPORT_CATALOG
from slugify import slugify


def get_report_filename(self, report):
    """Generate the filename for the sample PDF
    sample ID_MRN_pt name_ward

    e.g. PB22A012_TA000314_Minnie Mouse_ED
    :return:
    """
    sample = report.getAnalysisRequest()
    ward = sample.getWard()
    parts = [
        api.get_id(sample),
        sample.getMedicalRecordNumberValue() or "",
        sample.getPatientFullName() or "",
        api.get_title(ward) if ward else "",
        ]
    parts = [slugify(prt, separator="-", lowercase=False) for prt in parts]
    filename = "_".join(parts)
    return "{}.pdf".format(filename)


def __init__(self, context, request):
    super(ReportsListingView, self).__init__(context, request)

    self.catalog = REPORT_CATALOG
    self.contentFilter = {
        "portal_type": "ARReport",
        "path": {
            "query": api.get_path(self.context),
            "depth": 2,
        },
        "sort_on": "created",
        "sort_order": "descending",
    }

    self.form_id = "reports_listing"
    self.title = _("Analysis Reports")

    self.icon = "{}/{}".format(
        self.portal_url,
        "++resource++bika.lims.images/report_big.png"
    )
    self.context_actions = {}

    self.allow_edit = False
    self.show_select_column = True
    self.show_workflow_action_buttons = True
    self.pagesize = 30

    self.columns = collections.OrderedDict((
        ("Info", {
            "title": "",
            "toggle": True},),
        ("AnalysisRequest", {
            "title": _("Primary Sample"),
            "index": "sortable_title"},),
        ("Batch", {
            "title": _("Batch")},),
        ("PatientName", {
            "title": _("Patient")},),
        ("State", {
            "title": _("Review State")},),
        ("PDF", {
            "title": _("Download PDF")},),
        ("FileSize", {
            "title": _("Filesize")},),
        ("Date", {
            "title": _("Published Date")},),
        ("PublishedBy", {
            "title": _("Published By")},),
        ("Sent", {
            "title": _("Email sent")},),
        ("Recipients", {
            "title": _("Recipients")},),
    ))

    self.review_states = [
        {
            "id": "default",
            "title": "All",
            "contentFilter": {},
            "columns": self.columns.keys(),
            "custom_transitions": [],
        },
    ]


def folderitem(self, obj, item, index):
    """Adding PatientName Column in Augment folder listing
    """

    obj = api.get_object(obj)
    ar = obj.getAnalysisRequest()
    uid = api.get_uid(obj)
    review_state = api.get_workflow_status_of(ar)
    status_title = review_state.capitalize().replace("_", " ")

    # Report Info Popup
    # see: bika.lims.site.coffee for the attached event handler
    item["Info"] = get_link(
        "analysisreport_info?report_uid={}".format(uid),
        value="<i class='fas fa-info-circle'></i>",
        css_class="overlay_panel")

    item["replace"]["AnalysisRequest"] = get_link(
        ar.absolute_url(), value=ar.Title()
    )

    # Include Batch information of the primary Sample
    batch_id = ar.getBatchID()
    item["Batch"] = batch_id
    if batch_id:
        batch = ar.getBatch()
        item["replace"]["Batch"] = get_link(
            batch.absolute_url(), value=batch.Title()
        )

    pdf = self.get_pdf(obj)
    filesize = self.get_filesize(pdf)
    if filesize > 0:
        url = "{}/download_pdf".format(obj.absolute_url())
        item["replace"]["PDF"] = get_link(
            url, value="PDF", target="_blank")

    patient_name = ar.getPatientFullName()
    item["PatientName"] = patient_name

    item["State"] = _BMF(status_title)
    item["state_class"] = "state-{}".format(review_state)
    item["FileSize"] = "{:.2f} Kb".format(filesize)
    fmt_date = self.localize_date(obj.created())
    item["Date"] = fmt_date
    item["PublishedBy"] = self.user_fullname(obj.Creator())

    item["Sent"] = _("No")
    if obj.getSendLog():
        item["Sent"] = _("Yes")

    # N.B. There is a bug in the current publication machinery, so that
    # only the primary contact get stored in the Attachment as recipient.
    #
    # However, we're interested to show here the full list of recipients,
    # so we use the recipients of the containing AR instead.
    recipients = []

    for recipient in self.get_recipients(ar):
        email = safe_unicode(recipient["EmailAddress"])
        fullname = safe_unicode(recipient["Fullname"])
        if email:
            value = u"<a href='mailto:{}'>{}</a>".format(email, fullname)
            recipients.append(value)
        else:
            message = _("No email address set for this contact")
            value = u"<span title='{}' class='text text-danger'>" \
                    u"⚠ {}</span>".format(message, fullname)
            recipients.append(value)

    item["replace"]["Recipients"] = ", ".join(recipients)

    # No recipient with email set preference found in the AR, so we also
    # flush the Recipients data from the Attachment
    if not recipients:
        item["Recipients"] = ""

    return item

