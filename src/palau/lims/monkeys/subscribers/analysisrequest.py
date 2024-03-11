# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from bika.lims import api
from senaite.patient import api as patient_api
from senaite.patient import logger
from senaite.patient.subscribers.analysisrequest import get_patient_fields


def update_patient(instance):
    """Monkey patch of `update_patient` from patient.subscribers.
    Creates a new patient even if the MRN is temporary
    """
    mrn = instance.getMedicalRecordNumberValue()
    # Allow empty value when patients are not required for samples
    if mrn is None:
        return
    patient = patient_api.get_patient_by_mrn(mrn, include_inactive=True)
    # Create a new patient
    if patient is None:
        if patient_api.is_patient_allowed_in_client():
            # create the patient in the client
            container = instance.getClient()
        else:
            # create the patient in the global patients folder
            container = patient_api.get_patient_folder()

        # check if the user is allowed to add a new patient
        if not patient_api.is_patient_creation_allowed(container):
            return None

        logger.info("Creating new Patient in '{}' with MRN: '{}'"
                    .format(api.get_path(container), mrn))
        values = get_patient_fields(instance)
        try:
            patient = api.create(container, "Patient")
            patient_api.update_patient(patient, **values)
        except ValueError as exc:
            logger.error("%s" % exc)
            logger.error("Failed to create patient for values: %r" % values)
            raise exc
    return patient
