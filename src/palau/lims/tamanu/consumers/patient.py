# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2020-2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from senaite.jsonapi.api import deactivate_object
from senaite.jsonapi.interfaces import IPushConsumer
from senaite.patient import api as patient_api
from zope import interface

TAMANU_SEXES = (
    ("male", "m"),
    ("female", "f"),
    ("", ""),
)


class PatientPushConsumer(object):
    """Adapter that handles push requests for Patients
    """
    interface.implements(IPushConsumer)

    def __init__(self, data):
        self.data = data

    def process(self):
        """Creates objects from Patient type based on the data provided
        """
        patients = self.get_patients_data(self.data)
        link_patients = []
        for patient_data in patients:
            # Get replaced patient
            is_replaced = self.is_replaced(patient_data['resource'])

            patient = self.create_patient(patient_data, is_replaced)

            if is_replaced:
                replacement_patient_mrn = self.get_replacement_patient_mrn(
                    patient_data['resource']
                )
                link_patients.append({
                    "replacement_mrn": replacement_patient_mrn,
                    "original": patient
                })

        for link_patient in link_patients:
            self.update_replaced_patient(link_patient)

        return True

    def get_patients_data(self, data):
        """Get list of patients from payload
        """
        return data.get("patients", [])

    def is_replaced(self, patient_resource):
        """Check the patient is replaced
        """
        is_replaced = False
        links = patient_resource.get("link")
        if any(link.get("type") == "replaced-by" for link in links):
            is_replaced = True
        return is_replaced

    def get_replacement_patient_mrn(self, patient_resource):
        links = patient_resource.get("link")
        link_info = next((
            link.get("other") for link in links
            if link.get("type") == "replaced-by"
        ), None)
        replacement_patient_mrn = link_info.get("display", None)

        return replacement_patient_mrn

    def get_patient_fullname(self, patient_names):
        """Get patient's full name from resource payload
        """
        fullname = next((
            name for name in patient_names
            if name["use"] == "official"
        ), None)
        return fullname

    def get_patient_givenname(self, fullname):
        """Get patient's given name from full name
        """
        if fullname:
            return fullname.get("given", "")
        return ""

    def get_patient_address(self, patient_addresses):
        """Get patient's address from resource payload
        """
        address = next((
            patient_address for patient_address in patient_addresses
            if patient_address["type"] == "physical"
               and patient_address["use"] == "home"
        ), None)
        return address

    def get_patient_primary_phone_number(self, patient_telecoms):
        """Get patient's primary phone number from resource payload
        """
        phone = None
        for contact in patient_telecoms:
            if contact["rank"] != 1:
                continue
            phone = contact["value"]
        return phone

    def get_patient_secondary_phone_numbers(self, patient_telecoms):
        """Get patient's secondary phone number from resource payload
        """
        numbers = set()
        for contact in patient_telecoms:
            if contact["rank"] != 2:
                continue
            phone = contact["value"]
            numbers.add(phone)
        return filter(None, list(numbers))

    def get_patient_info(self, patient_resource):
        """Convert to patient dict from patient object data
        """
        sexes = dict(TAMANU_SEXES)

        usual_identifier = next(iter(
            filter(
                lambda x: x["use"] == "usual",
                patient_resource['identifier']
            )
        ))
        mrn = usual_identifier.get("value")
        sex = sexes[patient_resource.get("gender", "")]
        fullname = self.get_patient_fullname(patient_resource["name"])
        givenname = self.get_patient_givenname(fullname)
        firstname = givenname[0] if givenname != "" else ""
        middlename = (
            givenname[1]
            if givenname != "" and len(givenname) == 2 else ""
        )
        lastname = fullname.get("family", "")
        birthdate = patient_resource.get("birthDate", None)
        phone = self.get_patient_primary_phone_number(
            patient_resource["telecom"]
        )
        phones = self.get_patient_secondary_phone_numbers(
            patient_resource["telecom"]
        )
        additional_phone_numbers = [
            {"name": "Mobile", "phone": phone} for phone in phones
        ]
        address = self.get_patient_address(patient_resource["address"])

        if address:
            address_line = address.get("line", [""])
            address = list([{
                "type": api.safe_unicode(address.get("type", "")),
                "address": (
                    api.safe_unicode(address_line[0]) if address_line else ""
                ),
                "city": api.safe_unicode(address.get("city", "")),
            }])

        return {
            "mrn": mrn,
            "sex": sex,
            "birthdate": birthdate,
            "address": address,
            "gender": "",
            "firstname": api.safe_unicode(firstname),
            "middlename": api.safe_unicode(middlename),
            "lastname": api.safe_unicode(lastname),
            "phone": api.safe_unicode(phone),
            "additional_phone_numbers": additional_phone_numbers,
        }

    def create_patient(self, patient_data, is_replaced):
        patient_resource = patient_data['resource']
        patient_info = self.get_patient_info(patient_resource)
        patient = patient_api.get_patient_by_mrn(
            patient_info["mrn"], include_inactive=True
        )
        if not patient:
            container = patient_api.get_patient_folder()
            patient = api.create(container, "Patient", **patient_info)
        else:
            if not is_replaced:
                api.edit(patient, **patient_info)

        return patient

    def update_replaced_patient(self, link_patient):
        original = link_patient.get("original")
        replacement_mrn = link_patient.get("replacement_mrn")
        replacement_patient = patient_api.get_patient_by_mrn(
            replacement_mrn, include_inactive=True
        )
        replaced_by_info = {
            "replaced_by": replacement_patient
        }
        if api.get_review_status(original) == "active":
            api.edit(original, **replaced_by_info)
            deactivate_object(original)
