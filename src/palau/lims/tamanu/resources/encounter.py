# -*- coding: utf-8 -*-

from palau.lims.tamanu.resources import TamanuResource


class Encounter(TamanuResource):
    """Object that represents an Encounter resource from Tamanu
    """

    def getLocation(self):
        """Returns the Location resource assigned to this Encounter, if any
        """
        return self.get("subject")

    def getServiceProvider(self):
        """Returns the ServiceProvider resource assigned to this Encounter
        """
        return self.get("serviceProvider")
