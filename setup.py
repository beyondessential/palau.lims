# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023-2025 Beyond Essential Systems Pty. Ltd.

from setuptools import setup, find_packages

version = "1.0.0"

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("docs/changelog.rst", "r") as fh:
    long_description += "\n\n"
    long_description += fh.read()

setup(
    name="palau.lims",
    version=version,
    description="SENAITE extension profile aimed for health centers at "
                "Republic of Palau",
    long_description=open("README.rst").read(),
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "Framework :: Zope2",
    ],
    keywords="",
    author="NARALABS",
    author_email="info@naralabs.com",
    url="https://github.com/beyondessential/palau.lims",
    license="GPLv2",
    packages=find_packages("src", include=("palau*",)),
    package_dir={"": "src"},
    namespace_packages=["palau"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "bes.lims>=1.0.0",
        "requests",
        "senaite.storage>=2.6.0",
        # senaite.core does no longer provides schemaextender
        # https://github.com/senaite/senaite.core/pull/1931
        "archetypes.schemaextender",
        # Python 2.7: python-slugify < 5.0.0
        # Python 3.6+: python-slugify >= 5.0.0
        "python-slugify < 5.0.0",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "unittest2",
        ]
    },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
