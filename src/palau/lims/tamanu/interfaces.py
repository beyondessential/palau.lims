# -*- coding: utf-8 -*-

from zope.interface import Interface


class ITamanuResource(Interface):
    """Marker interface for a Tamanu's HL7 reosurce
    """

    def UID(self):
        """Returns the Tamanu UID of this resource
        """


class ITamanuContent(Interface):
    """Marker interface for objects that keep a reference to a counterpart
    content at Tamanu
    """
