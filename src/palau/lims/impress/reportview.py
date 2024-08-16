# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

import copy

import collections
import json
from bika.lims import api
from bika.lims.api import mail
from bika.lims.utils import get_link
from bika.lims.workflow import getTransitionActor
from bika.lims.workflow import getTransitionDate
from collections import OrderedDict
from palau.lims import messageFactory as _
from palau.lims.utils import get_field_value
from palau.lims.utils import get_initials
from palau.lims.utils import is_reportable
from plone.memoize import view
from senaite.ast.config import IDENTIFICATION_KEY
from senaite.ast.config import RESISTANCE_KEY
from senaite.ast.utils import is_ast_analysis
from senaite.core.api import dtime
from senaite.core.p3compat import cmp
from senaite.impress.analysisrequest.reportview import SingleReportView
from senaite.impress.decorators import returns_super_model
from senaite.patient import api as patient_api
from senaite.patient.config import SEXES
from senaite.patient.i18n import translate as patient_translate
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
        return patient_translate(sex)

    def get_department(self, sample):
        """Returns the Department title
        """
        sample = api.get_object(sample)
        department = sample.getWardDepartment()
        if not department:
            return ""
        return api.get_title(department)

    def get_analyses(self, model_or_collection, parts=False):
        """Returns a flat list of all analyses for the given model or
        collection, but only those in a "reportable" status are returned.
        If "parts" is False, analyses from partitions won't be included
        """
        analyses = super(SingleReportView, self).get_analyses(
            model_or_collection)

        sample_uid = api.get_uid(model_or_collection)  # noqa

        def get_growth_number(a, b):
            ast = [is_ast_analysis(a), is_ast_analysis(b)]
            if not all(ast):
                # do not apply sorting unless both analyses are from ast type
                return 0

            # Sort by growth number
            ga = a.getGrowthNumber()
            gb = b.getGrowthNumber()
            return cmp(ga, gb)

        # Sort AST analyses by growth number
        analyses = sorted(analyses, cmp=get_growth_number)

        # Remove non-reportable analyses
        analyses = filter(is_reportable, analyses)

        def is_from_primary(analysis):
            return analysis.getRequestUID() == sample_uid

        if not parts:
            # Remove analyses from partitions
            analyses = filter(is_from_primary, analyses)

        return analyses

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

        # If a retest, append the original
        invalidated = model.getInvalidated()
        if invalidated:
            samples.append(invalidated)

        # extend with current only if it contains "valid" tests
        sample = api.get_object(model)
        analyses = sample.objectValues("Analysis")
        analyses = filter(is_reportable, analyses)
        if analyses:
            samples.append(sample)

        # Extend with partitions
        parts = self.get_undergoing_partitions(sample)
        samples.extend(parts)

        return samples

    def get_analyses_by_category(self, model_or_collection, parts=False):
        """Return analyses grouped by category. If "parts" is False, analyses
        from partitions won't be returned
        """
        analyses = self.get_analyses(model_or_collection, parts=parts)
        return self.group_items_by("Category", analyses)

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

    def get_normal_values(self, model, analysis):
        """Returns the normal values that apply for the given analysis. Returns
        the formatted specification if value entered into min/max. Otherwise,
        returns the value entered into "Out of range comment" field
        """
        specs = analysis.getResultsRange()
        range_max = api.to_float(specs.get("max"), default=0)
        if range_max > 0:
            return model.get_formatted_specs(analysis)
        return specs.get("rangecomment")

    def get_analysis_conditions(self, analysis):
        """Returns the analysis conditions of the given analysis
        """
        # analysis (pre)conditions
        analysis = api.get_object(analysis)
        conditions = analysis.getConditions()
        return filter(None, map(self.format_condition, conditions))

    def get_analysis_footnotes(self, analysis):
        items = []
        analysis = api.get_object(analysis)

        # analysis (pre)conditions
        conditions = self.get_analysis_conditions(analysis)
        if conditions:
            items.append({"type": "conditions", "data": conditions})

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

    def get_result_variables_titles(self, analyses, report_only=True):
        """Returns the titles of the results variables for the given analyses
        """
        if not analyses:
            return []
        if not isinstance(analyses, (list, tuple)):
            analyses = [analyses]

        titles = []
        for analysis in analyses:
            for interim in self.get_result_variables(analysis, report_only):
                titles.append(interim.get("title"))
        return list(OrderedDict.fromkeys(titles))

    def get_user_properties(self, user):
        # Basic user information
        user = api.get_user(user)
        properties = api.get_user_properties(user)
        properties.update({
            "userid": user.getId(),
            "username": user.getUserName(),
            "roles": user.getRoles(),
            "email": user.getProperty("email"),
            "fullname": user.getProperty("fullname") or user.getUserName(),
            "salutation": "",
            "job_title": "",
        })
        # Overwrite with contact information
        contact = api.get_user_contact(user, contact_types=["LabContact"])
        if not contact:
            return properties

        fullname = contact.getFullname()
        if fullname:
            properties["fullname"] = fullname

        email_address = contact.getEmailAddress()
        if email_address:
            properties["email"] = email_address

        properties["salutation"] = contact.getSalutation()
        properties["job_title"] = contact.getJobTitle()
        return properties

    def get_verified_analyses(self, model):
        """Returns the valid analyses that were once verified
        """
        statuses = ["published", "verified"]
        return model.getAnalyses(full_objects=True, review_state=statuses)

    def get_submitted_analyses(self, model):
        """Returns the valid analyses that were once submitted
        """
        statuses = ["published", "verified", "to_be_verified"]
        return model.getAnalyses(full_objects=True, review_state=statuses)

    @view.memoize
    def get_verifiers(self, model):
        """Returns a dictionary where the keys are the username of the person
        who verified the sample, partitions or analyses and the value is the
        last verification date performed by the user
        """
        # get the verifier and date from the sample
        sample = api.get_object(model)

        # get the verifiers and dates from partitions
        partitions = self.get_undergoing_partitions(sample)

        # get the verifiers and dates from analyses
        analyses = self.get_verified_analyses(sample)

        # extract the verifiers and dates
        verifiers = {}
        items = [sample] + partitions + analyses
        for item in items:
            verifier = self.get_action_user(item, "verify")
            verified = self.get_action_date(item, "verify")
            if not all([verifier, verified]):
                continue

            last_verified = verifiers.get(verifier)
            if not last_verified or verified > last_verified:
                verifiers[verifier] = verified

        return verifiers

    @view.memoize
    def get_submitters(self, model):
        """Returns a dictionary where the keys are the username of the person
        who submitted the sample, partitions or analyses and the value is the
        last submission date performed by the user
        """
        # get the submitter and date from the sample
        sample = api.get_object(model)

        # get the submitters and dates from partitions
        partitions = self.get_undergoing_partitions(sample)

        # get the submitters and dates from analyses
        analyses = self.get_submitted_analyses(sample)

        # extract the submitters and dates
        submitters = {}
        items = [sample] + partitions + analyses
        for item in items:
            submitter = self.get_action_user(item, "submit")
            submitted = self.get_action_date(item, "submit")
            if not all([submitter, submitted]):
                continue

            last_submitted = submitters.get(submitter)
            if not last_submitted or submitted > last_submitted:
                submitters[submitter] = submitted

        return submitters

    @view.memoize
    def get_submitters_info(self, model):
        """Returns a list made of dicts representing the LabContacts (or users)
        that submitted at least one analysis
        """
        info = []
        submitters = self.get_submitters(model)
        for submitter, submitted in submitters.items():
            props = self.get_user_properties(submitter)
            props["submitted"] = submitted
            info.append(props)
        return info

    @view.memoize
    def get_verifiers_info(self, model):
        """Returns a list made of dicts representing the LabContacts (or users)
        that verified at least one analysis
        """
        info = []
        verifiers = self.get_verifiers(model)
        for verifier, verified in verifiers.items():
            props = self.get_user_properties(verifier)
            props["verified"] = verified
            info.append(props)
        return info

    def get_results_interpretations(self, model):
        """Returns the result interpretations
        """
        # do a hard copy to prevent persistent changes
        interpretations = copy.deepcopy(model.getResultsInterpretationDepts())

        # group by user
        groups = collections.OrderedDict()
        for interpretation in interpretations:
            user = interpretation.get("user", "")
            groups.setdefault(user, []).append(interpretation)

        out = []
        for user, items in groups.items():
            # get the comments from this user
            comments = [item.get("richtext", "").strip() for item in items]
            # bail out those with no value or empty
            comments = filter(None, comments)
            if not comments:
                continue

            out.append({
                "user": user,
                "initials": get_initials(user),
                "richtext": "".join(comments),
            })

        return out

    def get_action_user(self, model, action_id):
        """Returns the user who last performed the given action for the model
        """
        obj = api.get_object(model)
        return getTransitionActor(obj, action_id)

    def get_action_date(self, model, action_id):
        """Returns the last time the given action for model took place
        """
        obj = api.get_object(model)
        return getTransitionDate(obj, action_id, return_as_datetime=True)

    def is_out_of_stock(self, analysis):
        """Returns whether the analysis passed-in is out-of-stock
        """
        return api.get_review_status(analysis) == "out_of_stock"

    @view.memoize
    def get_undergoing_partitions(self, sample):
        """Returns the partitions of the sample that are undergoing
        """
        partitions = []
        skip = ["cancelled", "invalid", "rejected", "stored", "dispatched"]
        for partition in sample.getDescendants(all_descendants=True):
            # skip partitions that are not in a valid status
            if api.get_review_status(partition) in skip:
                continue

            # do not include partitions without "valid" tests
            analyses = partition.getAnalyses(full_objects=True)
            analyses = filter(is_reportable, analyses)
            if not analyses:
                continue

            partitions.append(partition)
        return partitions

    @view.memoize
    def is_provisional(self, model):
        """Returns whether the model (partitions included) is provisional
        """
        sample = api.get_object(model)
        if sample.isInvalid():
            return True

        valid_statuses = ['verified', 'published']
        status = api.get_review_status(sample)
        if status not in valid_statuses:
            return True

        # find out partitions
        for partition in self.get_undergoing_partitions(sample):
            status = api.get_review_status(partition)
            if status not in valid_statuses:
                return True

        return False

    @view.memoize
    def get_verified_date(self, model):
        """Returns the last verification date from the analyses and sample
        """
        verifiers = self.get_verifiers(model)
        if not verifiers:
            return None
        return max(verifiers.values())

    @view.memoize
    def get_submitted_date(self, model):
        """Returns the last submitted date from the sample and partitions
        """
        submitters = self.get_submitters(model)
        if not submitters:
            return None
        return max(submitters.values())
