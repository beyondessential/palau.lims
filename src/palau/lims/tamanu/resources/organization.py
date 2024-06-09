# -*- coding: utf-8 -*-

from palau.lims.tamanu.resources import TamanuResource


class Organization(TamanuResource):
    """Object that represents an Organization resource from Tamanu
    """

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
