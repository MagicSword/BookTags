#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~
    init
    :copyright: 2019 Miller
    :license: BSD-3-Clause
"""

# Known bugs that can't be fixed here:
#   - synopsis() cannot be prevented from clobbering existing
#     loaded modules.
#   - If the __file__ attribute on a module is a relative path and
#     the current directory is changed with os.chdir(), an incorrect
#     path will be displayed.

import os

# --------------------------------------------------------- common routines
USER_HOME = os.path.expanduser("~")
# PROJECT_DIR = os.path.join(USER_HOME, ".booktags")
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
# Project-wide setting

# if not os.path.exists(PROJECT_DIR):
#     os.makedirs(PROJECT_DIR)

if __name__ == '__main__':
    pass