# -*- coding: utf-8 -*-

from bika.lims import api
from bika.lims.api import UID_CATALOG
from palau.lims.tamanu.consumers.patient import TAMANU_SEXES
from palau.lims.tamanu.resources import TamanuResource

_marker = object()


class PatientResource(TamanuResource):

    def search(self, field_name=None):
        """Search
        """
        tamanu_uid = self.get("id")
        if field_name:
            record = self.get_raw(field_name, _marker)
            if self.is_reference(record):
                obj = self.get_reference(record)
                tamanu_uid = obj.get("id")
        results = self.search_by_uid(tamanu_uid)
        return results

    def search_by_uid(self, uid=None):
        """Search
        """
        query = {"tamanu_uid": uid}
        results = api.search(query, catalog=UID_CATALOG)
        if len(results) > 0:
            return api.get_object(results[0])
        return None

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
               and patient_address["use"] == "home"  # noqa
        ), None)
        return address

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
        }
