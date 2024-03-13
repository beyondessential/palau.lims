# -*- coding: utf-8 -*-

from bika.lims import api
from palau.lims.tamanu.config import TAMANU_SEXES
from palau.lims.tamanu.resources import TamanuResource

_marker = object()


class PatientResource(TamanuResource):

    def get_fullname(self):
        """Get patient's full name from resource payload
        """
        patient_names = self.get("name")
        fullname = next((
            name for name in patient_names
            if name.get("use") == "official"
        ), None)
        return fullname

    def get_givenname(self):
        """Get patient's given name from full name
        """
        fullname = self.get_fullname()
        if fullname:
            return fullname.get("given", "")
        return ""

    def get_address(self):
        """Get patient's address from resource payload
        """
        patient_addresses = self.get("address")
        address = next((
            patient_address for patient_address in patient_addresses
            if patient_address.get("type") == "physical"
               and patient_address.get("use") == "home"  # noqa
        ), None)
        return address

    def to_object_info(self):
        """Returns a dict representation of the Patient resource, suitable for
        the creation and edition of SENAITE Patient objects
        """
        sexes = dict(TAMANU_SEXES)

        usual_identifier = next(iter(
            filter(
                lambda x: x.get("use") == "usual",
                self.get('identifier')
            )
        ))
        mrn = usual_identifier.get("value")
        sex = sexes.get(self.get("gender")) or ""
        fullname = self.get_fullname()
        givenname = self.get_givenname()
        firstname = givenname[0] if givenname != "" else ""
        middlename = (
            givenname[1]
            if givenname != "" and len(givenname) == 2 else ""
        )
        lastname = fullname.get("family", "")
        birthdate = self.get("birthDate")
        address = self.get_address()

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
            "portal_type": "Patient",
        }
