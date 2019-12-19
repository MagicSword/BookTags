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

import os

# from ..config_proj import Config,DevelopmentConfig
#
#
# # --------------------------------------------------------- common routines
#
# class DevelopmentConfig(DevelopmentConfig):
#     DEBUG = True
#     # DB_name = "booktags-dev.sqlite"
#     # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Project_HOME, DB_name)
#
#
# class TestingConfig(Config):
#     TESTING = True
#     # DB_name = "booktags-test.sqlite"
#     # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Project_HOME, DB_name)
#
#
# class ProductionConfig(Config):
#     # DB_name = "booktags.sqlite"
#     # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Project_HOME, DB_name)
#     pass
#
#
#
# config = {
#     'development' : DevelopmentConfig,
#     'testing' : TestingConfig,
#     'production' : ProductionConfig,
#     'default' : DevelopmentConfig
# }

if __name__ == '__main__':
    pass