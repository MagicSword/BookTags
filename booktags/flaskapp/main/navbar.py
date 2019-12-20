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

# TODO : fix flask_nav
import abc
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator

# --------------------------------------------------------- common routines

nav = Nav()

# registers the "top" menubar
nav.register_element('top', Navbar(
    View('Widgits, Inc.', 'index'),
    View('Our Mission', 'about'),
    Subgroup(
        'Products',
        View('Wg240-Series', 'products', product='wg240'),
        View('Wg250-Series', 'products', product='wg250'),
        Separator(),
        Text('Discontinued Products'),
        View('Wg10X', 'products', product='wg10x'),
    )

))


if __name__ == '__main__':
    pass