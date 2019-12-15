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

#from .main.navbar import nav
#from config import Config

# --------------------------------------------------------- common routines

def create_app():
    # Initialize Flask instance
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'devkeys'
    # Initialize  Blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # Initialize Bootstrap
    Bootstrap(app)
    moment  = Moment(app)

    # Initialize Nav
    # TODO: fix flask_navbar
    #nav.init_app(app)

    # return app
    return app


if __name__ == '__main__':
    pass