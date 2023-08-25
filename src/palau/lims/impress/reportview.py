# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import copy
import json

from bika.lims import api
from bika.lims.api import mail
from bika.lims.utils import get_link
from Products.CMFPlone.utils import safe_unicode
from palau.lims import messageFactory as _
from palau.lims.utils import get_field_value
from senaite.ast.config import IDENTIFICATION_KEY
from senaite.ast.config import RESISTANCE_KEY
from senaite.ast.utils import is_ast_analysis
from senaite.core.api import dtime
from senaite.impress.analysisrequest.reportview import SingleReportView
from senaite.impress.decorators import returns_super_model
from senaite.patient import api as patient_api
from senaite.patient.config import SEXES
from weasyprint.compat import base64_encode


BOOL_TEXTS = {True: _("Yes"), False: _("No")}


class DefaultReportView(SingleReportView):
    """Product-specific controller view for multiple results reports
    """

    def long_date(self, date):
        """Returns the localized date in long format
        """
        return self.to_localized_time(date, long_format=1)

    def short_date(self, date):
        """Returns the localized date in short format
        """
        return self.to_localized_time(date, long_format=0)

    def get_client_logo_src(self, client):
        """Returns the src suitable for embedding into img html element of the
        client's logo, if any. Returns None otherwise
        """
        logo = client.ReportLogo
        if not logo:
            return None
        return self.get_image_blob_src(logo)

    def get_lab_logo_src(self):
        """Returns the src suitable for embedding into img html element of the
        laboratory's logo, if any. Returns None otherwise
        """
        setup = api.get_setup()
        logo = get_field_value(setup, "ReportLogo")
        return self.get_image_blob_src(logo)

    def get_image_blob_src(self, img):
        """Returns the src suitable for embedding into html element
        """
        if not img:
            return None
        data_url = "data:"+img.content_type+";base64," + (
            base64_encode(img.data).decode("ascii").replace("\n", ""))
        return data_url

    def get_email_address(self, contact):
        """Returns the email address of the contact as a pair format
        """
        name = contact.getFullname() or ""
        email = contact.getEmailAddress()
        if not email:
            return name
        return mail.to_email_address(email, name)

    def get_age(self, dob, onset_date=None):
        """Returns a string that represents the age in ymd format
        """
        try:
            delta = dtime.get_relative_delta(dob, onset_date)
            if delta.years >= 2:
                return "{}y".format(delta.years)
        except ValueError:
            # no valid date or dates
            return ""

        # Full ymd
        return patient_api.to_ymd(delta, default="")

    def is_estimated_age(self, sample):
        """Returns whether the age of the patient is estimated
        """
        dob_field = sample.getField("DateOfBirth")
        return dob_field.get_estimated(sample)

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

    def sort_items(self, items, reverse=False):
        """Sort items so that Microbiology category be at the end of the report
        for Urine sample type
        """
        def sortable_title(obj):
            sort_key = obj.get("SortKey") or 0.0
            title = obj.title.lower()
            return u"{:010.3f}{}".format(sort_key, safe_unicode(title))

        def _cmp(obj1, obj2):
            st1 = sortable_title(obj1)
            st2 = sortable_title(obj2)
            return cmp(st1, st2)

        def _cmp_urine(obj1, obj2):
            if api.get_title(obj1) == 'Microbiology':
                return 1
            if api.get_title(obj2) == 'Microbiology':
                return -1
            return _cmp(obj1, obj2)

        if self.model.getSampleTypeTitle() == 'Urine':
            return sorted(items, cmp=_cmp_urine, reverse=reverse)
        return sorted(items, cmp=_cmp, reverse=reverse)

    def get_analyses(self, model_or_collection, parts=False):
        """Returns a flat list of all analyses for the given model or
        collection, but only those in a "reportable" status are returned.
        If "parts" is False, analyses from partitions won't be included
        """
        analyses = super(SingleReportView, self).get_analyses(
            model_or_collection)

        sample_uid = api.get_uid(model_or_collection)

        def is_reportable(analysis):
            hidden = analysis.getHidden()
            if hidden:
                return False

            if not parts:
                # Skip partitions
                if analysis.getRequestUID() != sample_uid:
                    return False

            if is_ast_analysis(analysis):
                if analysis.getKeyword() != RESISTANCE_KEY:
                    return False

            reportable = ["to_be_verified", "verified", "published"]
            return api.get_review_status(analysis) in reportable

        return filter(is_reportable, analyses)

    @returns_super_model
    def get_ancestry(self, model):
        """Returns the whole lineage of primaries of the model passed-in,
        along with the model itself
        """
        def get_primaries(sample, primaries=None):
            if primaries is None:
                primaries = []
            primary = sample.getPrimaryAnalysisRequest()
            if primary:
                primaries.append(primary)
                return get_primaries(primary, primaries=primaries)
            return primaries

        # Extract all primaries of this sample
        samples = get_primaries(model)

        # Reverse them so the first primary is the oldest
        samples = list(reversed(samples))

        # Extend with current
        samples.append(model)

        # Extend with partitions
        parts = model.getDescendants(all_descendants=True)
        samples.extend(parts)

        return samples

    def get_analyses_by_category(self, model_or_collection, parts=False):
        """Return analyses grouped by category. If "parts" is False, analyses
        from partitions won't be returned
        """
        analyses = self.get_analyses(model_or_collection, parts=parts)
        return self.group_items_by("Category", analyses)

    def is_valid_status(self, analysis):
        """Returns whether the analysis object or brain is in a valid status
        """
        invalid = ["retracted", "rejected", "cancelled"]
        return api.get_review_status(analysis) not in invalid

    def is_results_in_progress(self, sample):
        """Returns true if there are analyses not yet verified
        """
        def in_progress(analysis):
            return not analysis.getDateVerified()

        # Exclude invalid analyses
        analyses = self.get_analyses(sample)
        analyses = filter(self.is_valid_status, analyses)

        # Ensure all valid analyses are in progress
        analyses = map(in_progress, analyses)
        return any(analyses)

    def get_formatted_result(self, sample_model, analysis):
        """Returns the result of the analysis properly formatted
        """
        if analysis.getKeyword() == RESISTANCE_KEY:
            # Return the result with the Sensitivity Category R/S/I prefixed
            result = analysis.getResult()

            # Extract the values and texts from result options
            choices = analysis.getResultOptions()

            # Set the category (R/I/S) as prefix
            def prefix_category(val):
                if ": " not in val:
                    return val
                idx = val.rindex(": ")
                category = val[idx+2:]
                if not category:
                    category = "?"
                return "{}: {}".format(category, val[:idx])

            choices_texts = map(lambda c: str(c["ResultText"]), choices)
            choices_texts = map(prefix_category, choices_texts)

            # Create a dict for easy mapping of result options
            choices_values = map(lambda c: str(c["ResultValue"]), choices)
            values_texts = dict(zip(choices_values, choices_texts))

            # Result might contain a single result option
            match = values_texts.get(str(result))
            if match:
                return match

            # Result is a string with multiple options e.g. "['2', '1']"
            try:
                raw_result = json.loads(result)
                texts = map(lambda r: values_texts.get(str(r)), raw_result)
                texts = filter(None, texts)
                return "<br/>".join(texts)
            except (ValueError, TypeError):
                pass

        if analysis.getKeyword() == IDENTIFICATION_KEY:
            # Display the growth number next to each microorganism
            interims = analysis.getInterimFields()
            growth = filter(lambda it: it.get("keyword") == "growth", interims)
            try:
                growth = growth and growth[0] or {}
                growth = json.loads(growth.get("value"))
            except (ValueError, TypeError):
                growth = []

            growth = growth or [""]

            # Raw result
            result = analysis.getResult()

            # Extract the values and texts from result options
            choices = analysis.getResultOptions()
            choices_texts = map(lambda c: str(c["ResultText"]), choices)

            # Create a dict for easy mapping of result options
            choices_values = map(lambda c: str(c["ResultValue"]), choices)
            values_texts = dict(zip(choices_values, choices_texts))

            # Result might contain a single result option
            match = values_texts.get(str(result))
            if match:
                if growth:
                    return "#{} {}".format(growth[0], match)

            # prepend '#' to growth numbers
            def prepend_hash(val):
                val = str(val).strip()
                if not val:
                    return ""
                return "#{}".format(val)
            growth = [prepend_hash(gr) for gr in growth]

            # Result is a string with multiple options e.g. "['2', '1']"
            try:
                raw_result = json.loads(result)
                texts = map(lambda r: values_texts.get(str(r)), raw_result)
                # extend growth list to have same length as texts
                growth = growth + [""]*(len(texts)-len(growth))
                texts = zip(growth, texts)
                texts = [" ".join(text) for text in texts]
                return "<br/>".join(texts)
            except (ValueError, TypeError):
                pass

        # Delegate to 'standard' formatted result resolver
        return sample_model.get_formatted_result(analysis)

    def get_analysis_footnotes(self, analysis):
        items = []
        analysis = api.get_object(analysis)

        # analysis (pre)conditions
        conditions = analysis.getConditions()
        conditions = filter(None, map(self.format_condition, conditions))
        if conditions:
            items.append({"type": "conditions", "data": conditions})

        # interim fields
        interims = self.get_result_variables(analysis)
        if interims:
            items.append({"type": "interims", "data": interims})

        # analysis remarks
        remarks = analysis.getRemarks()
        if remarks:
            items.append({"type": "remarks", "data": remarks})

        return items

    def is_true(self, val):
        """Returns whether val evaluates to True
        """
        val = str(val).strip().lower()
        return val in ["y", "yes", "1", "true", "on"]

    def format_condition(self, condition):
        """Returns an string representation of the analysis condition value
        """
        title = condition.get("title")
        value = condition.get("value", "")
        if not any([title, value]):
            return None

        condition_type = condition.get("type")
        if condition_type == "checkbox":
            value = BOOL_TEXTS.get(self.is_true(value))

        elif condition_type == "file":
            attachment = api.get_object_by_uid(value, None)
            if not attachment:
                return None
            value = self.get_attachment_link(attachment)

        return ": ".join([title, str(value)])

    def get_attachment_link(self, attachment):
        """Returns a well-formed link for the attachment passed in
        """
        filename = attachment.getFilename()
        att_url = api.get_url(attachment)
        url = "{}/at_download/AttachmentFile".format(att_url)
        return get_link(url, filename, tabindex="-1")
