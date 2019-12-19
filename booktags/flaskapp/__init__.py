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
#from flask_migrate import Migrate
#from .main.navbar import nav
from ..config_proj import config, DevelopmentConfig




# --------------------------------------------------------- common routines
# Initialize Bootstrap
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
# Initialize SQLAlchemy
db = SQLAlchemy()
#migrate = Migrate()



def create_app(config_name):
    # Initialize Flask instance
    app = Flask(__name__)
    # app.config.from_object(config[config_name])
    # config[config_name].init_app(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize Nav
    # TODO: fix flask_navbar
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    # db.create_all(app)
    #migrate.init_app(app,db)


    # Initialize  Blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # 指派 路由 ，錯誤頁面

    # return app
    return app


if __name__ == '__main__':
    pass