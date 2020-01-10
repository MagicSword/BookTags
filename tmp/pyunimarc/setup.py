# -*- coding: utf-8 -*-

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

import os
from os import path as osp

HERE = osp.dirname(osp.abspath(__file__))

with open(osp.join(HERE, "README.rst")) as inp:
    long_description = inp.read()

setup(
    name="pyunimarc",
    version="0.1.0",
    description="Unimarc reader",
    long_description=long_description,
    url="https://forge.extranet.logilab.fr/open-source/pyunimarc",
    author="Logilab",
    author_email="contact@logilab.fr",
    license="LGPL",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Markup",
        "Programming Language :: Python :: 3",
    ],

    packages=find_packages(),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip"s
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={},

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={},
)
