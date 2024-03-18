# -*- coding: utf-8 -*-


SALUTATIONS = ("dr", "mr", "ms", "mx")


class HumanName(dict):
    """Object that represents an HL7 HumanName datatype
    https://www.hl7.org/fhir/datatypes.html#humanname
    """

    def get_name_info(self):
        """Returns a dict with the name parts
        """
        info = {
            "Salutation": "",
            "Firstname": "",
            "Middleinitial": "",
            "Middlename": "",
            "Surname": "",
        }

        family = self.get("familyName")
        given = self.get("given")
        if family and given:
            info.update({
                "Salutation": self.get("prefix"),
                "Firstname": given[0],
                "Surname": family,
                "Middlename": " ".join(given[1:]),
            })
            return info

        # Rely on the 'text' entry
        fullname = self.get("text")
        parts = filter(None, fullname.split(" "))
        if not parts:
            return info

        if len(parts) == 1:
            info["Firstname"] = parts[0]
            return info

        if parts[0].strip(".").lower() in SALUTATIONS:
            info["Salutation"] = parts[0]
            parts = parts[1:]

        info["Firstname"] = parts[0]
        info["Surname"] = " ".join(parts[1:])
        return info
