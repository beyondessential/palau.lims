# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from palau.lims import logger


def disable_field(schema, field_id):
    """Hides and makes the schema field for the given id as non required
    """
    schema[field_id].required = False
    schema[field_id].widget.visible = False


def update_field(schema, field_id, field_info):
    """Updates the schema field for with the field_info provided
    """
    # Field properties
    field = schema[field_id]
    field.schemata = field_info.get("schemata", field.schemata)
    props = filter(lambda f: f != "widget", field_info.keys())
    for prop_id in props:
        if not hasattr(field, prop_id):
            logger.warn("Field property {} is missing".format(prop_id))
            continue
        setattr(field, prop_id, field_info.get(prop_id))
        if prop_id == "validators":
            # Resolve the validator is in the service
            field._validationLayer()

    # Widget properties
    widget = field.widget
    props = field_info.get("widget", {})
    if isinstance(props, dict):
        for prop_id, prop_value in props.items():
            if not hasattr(widget, prop_id):
                logger.warn("Widget Property {} is missing".format(prop_id))
                continue
            setattr(widget, prop_id, prop_value)
    elif props:
        field.widget = props


def disable_schemata(schema, schemata_id):
    """Disables all fields from the schemata id passed in
    """
    fields = filter(lambda f: f.schemata == schemata_id, schema.fields())
    map(lambda f: disable_field(schema, f.getName()), fields)
