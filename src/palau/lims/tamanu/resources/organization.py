# -*- coding: utf-8 -*-

from bika.lims import api
from palau.lims.tamanu import api as tapi
from palau.lims.tamanu.resources import TamanuResource


class Organization(TamanuResource):
    """Object that represents an Organization resource from Tamanu
    """

    _obj_uid = None

    def getObject(self):
        """Returns the counterpart SENAITE object of this Tamanu resource
        Mimics the behavior of DX and AT types
        """
        # TODO 'tamanu_uid' does not get indexed in UID catalog for AT???
        obj = api.get_object_by_uid(self._obj_uid, None)
        if obj:
            return obj

        obj = tapi.get_object_by_tamanu_uid(self.UID, default=None)
        if obj:
            self._obj_uid = api.get_uid(obj)
            return obj

        clients = api.get_portal().clients
        for client in clients.objectValues():
            if tapi.get_tamanu_uid(client) == self.UID:
                self._obj_uid = api.get_uid(client)

        return api.get_object_by_uid(self._obj_uid, None)

    def to_object_info(self):
        """Returns a dict representation of the Organization resource, suitable
        for the creation and edition of SENAITE's Organisation objects like
        Client, Supplier, Manufacturer, etc.
        """
        name = self.get("name")
        return {
            "Name": name,
            "title": name,
            "TaxNumber": "",
            "Phone": "",
            "Fax": "",
            "EmailAddress": "",
            "PhysicalAddress": {},
            "PostalAddress": {},
            "BillingAddress": {},
            "AccountType": "",
            "AccountName": "",
            "BankName": "",
            "BankBranch": "",
        }
