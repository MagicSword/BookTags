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
Project_HOME = os.path.join(USER_HOME, ".booktags")
SQL_ALCHEMY_CONN = "sqlite:///{}/booktags.sqlite"
SQL_ALCHEMY_CONN_PGSQL = "postgres+psycopg2://miller:ming22d@localhost:5432/booktags"


if not os.path.exists(Project_HOME):
    os.makedirs(Project_HOME)





if __name__ == '__main__':
    pass