# -*- coding: utf-8 -*-

from palau.lims.tamanu import logger
from senaite.core.setuphandlers import setup_core_catalogs
from senaite.core.setuphandlers import setup_other_catalogs

UID_CATALOG = "uid_catalog"

# Add-on specific Catalogs (list of core's BaseCatalog objects)
CATALOGS = (
)

# Tuples of (catalog, index_name, index_attribute, index_type)
INDEXES = [
    (UID_CATALOG, "tamanu_uid", "tamanu_uid", "FieldIndex"),
]

# Tuples of (catalog, column_name)
COLUMNS = [
]


def setup_catalogs(portal):
    """Setup new catalogs and modifications to existing ones
    """
    logger.info("Setup Catalogs ...")
    setup_core_catalogs(portal, catalog_classes=CATALOGS)
    setup_other_catalogs(portal, indexes=INDEXES, columns=COLUMNS)
    logger.info("Setup Catalogs [DONE]")
