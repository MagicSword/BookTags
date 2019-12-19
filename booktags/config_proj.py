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

from .logger import create_logger


USER_HOME = os.path.expanduser("~")
Project_HOME = os.path.join(USER_HOME, ".booktags")
# SQL_ALCHEMY_CONN_PGSQL = "postgres+psycopg2://miller:ming22d@localhost:5432/booktags"



class Config(object):
    """Common config

    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # logger = create_logger("")
    # logger.info('Start logging \n')
    #
    # try:
    #     pass
    # except Exception as e:
    #     logger.exception("Runtime Error Message:")

    # logger.info("Export Done!")

    # SQLALCHEMY_TRACK_MODIFICATONS = False
    DB_name = "booktags-dev.sqlite"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              "sqlite:///" + os.path.join(Project_HOME, DB_name)


class TestingConfig(Config):
    TESTING = True
    DB_name = "booktags-test.sqlite"
    SQLALCHEMY_DATABASE_URI =  os.environ.get('TEST_DATABASE_URL') or \
                               "sqlite:///" + os.path.join(Project_HOME, DB_name)


class ProductionConfig(Config):
    DB_name = "booktags.sqlite"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              "sqlite:///" + os.path.join(Project_HOME, DB_name)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

if not os.path.exists(Project_HOME):
    os.makedirs(Project_HOME)

if __name__ == '__main__':
    pass