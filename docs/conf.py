#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    example.py
    ~~~~~~~~~
    A simple command line application to run flask apps.
    :copyright: 2019 Miller
    :license: BSD-3-Clause
"""

# Known bugs that can't be fixed here:
#   - synopsis() cannot be prevented from clobbering existing
#     loaded modules.
#   - If the __file__ attribute on a module is a relative path and
#     the current directory is changed with os.chdir(), an incorrect
#     path will be displayed.

import abc


# --------------------------------------------------------- common routines

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]
# The name of the entry point, without the ".rst" extension.
# By convention this will be "index"
master_doc = "index"
# This values are all used in the generated documentation.
# Usually, the release and version are the same,
# but sometimes we want to have the release have an "rc" tag.
project = "Booktags"
copyright = "2019, Nero Miller"
author = "Nero Miller"
version = release = "2019.1.0"


[tox]
# By default, .tox is the directory.
# Putting it in a non-dot file allows opening the generated
# documentation from file managers or browser open dialogs
# that will sometimes hide dot files.
toxworkdir = {toxinidir}/build/tox

[testenv:docs]
# Running sphinx from inside the "docs" directory
# ensures it will not pick up any stray files that might
# get into a virtual environment under the top-level directory
# or other artifacts under build/
changedir = docs
# The only dependency is sphinx
# If we were using extensions packaged separately,
# we would specify them here.
# A better practice is to specify a specific version of sphinx.
deps =
    sphinx
# This is the sphinx command to generate HTML.
# In other circumstances, we might want to generate a PDF or an ebook
commands =
    sphinx-build -W -b html -d {envtmpdir}/doctrees . {envtmpdir}/html
# We use Python 3.7. Tox sometimes tries to autodetect it based on the name of
# the testenv, but "docs" does not give useful clues so we have to be explicit.
basepython = python3.7