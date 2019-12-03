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


import atexit

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import scoped_session, sessionmaker

from .. import SQL_ALCHEMY_CONN_PGSQL,SQL_ALCHEMY_CONN


engine = None
Session = None


def configure_orm():
    global engine
    global Session

    engine_args = {"poolclass": NullPool}
    engine = create_engine(SQL_ALCHEMY_CONN_PGSQL , **engine_args)
    Session = scoped_session(
        sessionmaker(
            autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
        )
    )


def dispose_orm():
    global engine
    global Session

    if Session is not None:
        Session.remove()
        Session = None
    if engine is not None:
        engine.dispose()
        engine = None


configure_orm()
atexit.register(dispose_orm)