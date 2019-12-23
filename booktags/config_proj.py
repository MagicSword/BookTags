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
    # Flask Mail setting
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.mailtrap.io')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '2525'))
    #MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "fd865060444122"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "48cd09b5c34f24"
    PROJECT_MAIL_SUBJECT_PREFIX = '[Booktags]'
    PROJECT_MAIL_SENDER = 'Project Admin <booktags@example.com>'
    # end Flask mail setting
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    PROJECT_ADMIN = os.environ.get('PROJECT_ADMIN')
    SSL_REDIRECT = False
    # PROJECT_ADMIN = "booktags@example.com"
    PROJECT_POSTS_PER_PAGE = 20
    PROJECT_FOLLOWERS_PER_PAGE = 50
    PROJECT_COMMENTS_PER_PAGE = 30
    PROJECT_SLOW_DB_QUERY_TIME = 0.5


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


    DB_name = "booktags-dev.sqlite"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              "sqlite:///" + os.path.join(Project_HOME, DB_name)


class TestingConfig(Config):
    TESTING = True
    DB_name = "booktags-test.sqlite"
    SQLALCHEMY_DATABASE_URI =  os.environ.get('TEST_DATABASE_URL') or \
                               "sqlite:///" + os.path.join(Project_HOME, DB_name)
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DB_name = "booktags.sqlite"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              "sqlite:///" + os.path.join(Project_HOME, DB_name)

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.PROJECT_MAIL_SENDER,
            toaddrs=[cls.PROJECT_ADMIN],
            subject=cls.PROJECT_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)




config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,

    'default': DevelopmentConfig
}

if not os.path.exists(Project_HOME):
    os.makedirs(Project_HOME)

if __name__ == '__main__':
    pass