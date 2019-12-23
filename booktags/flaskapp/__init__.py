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

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#from .main.navbar import nav
from flask_pagedown import PageDown
from ..config_proj import config
# --------------------------------------------------------- common routines
# Initialize
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    # Initialize Flask instance
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize Nav
    # TODO: fix flask_navbar
    login_manager.init_app(app)
    bootstrap.init_app(app)
    pagedown.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)



    # Initialize  Blueprint
    # main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # auth blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # api blueprint
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    # 指派 路由 ，錯誤頁面

    return app
