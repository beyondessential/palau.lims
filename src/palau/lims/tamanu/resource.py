# -*- coding: utf-8 -*-

from bika.lims import api
from bika.lims.api import UID_CATALOG
from palau.lims.tamanu.consumers.patient import TAMANU_SEXES
from palau.lims.tamanu.interfaces import ITamanuResource
from zope.interface import implementer


_marker = object()


@implementer(ITamanuResource)
class BaseResource(object):

    _refs = {}

    def __init__(self, session, data):
        self._session = session
        self._data = data

    def UID(self):
        """Returns the Tamanu UID of this resource
        """
        return self.get("id")

    def get_raw(self, field_name, default=None):
        return self._data.get(field_name, default)

    def is_reference(self, record):
        if not isinstance(record, dict):
            return False
        reference_id = record.get("reference")
        if reference_id:
            return True
        return False

    def get_reference(self, record_or_id):
        if isinstance(record_or_id, dict):
            ref_id = record_or_id.get("reference")
        else:
            ref_id = record_or_id
        reference = self._refs.get(ref_id)
        if not reference:
            reference = self._session.get(ref_id)
            self._refs[ref_id] = reference
        return self._refs[ref_id]

    def get(self, field_name, default=None):
        record = self.get_raw(field_name, _marker)
        if record is _marker:
            return default

        # is this record a reference
        if self.is_reference(record):
            return self.get_reference(record)

        return record

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

    def __repr__(self):
        return repr(self._data)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()
