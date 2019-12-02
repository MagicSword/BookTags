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

from . import main
from flask import render_template

# --------------------------------------------------------- common routines


@main.route('/')
@main.route('/index')
def index():
    print(__name__)
    print(__name__.split('.')[0])
    return "This is flask app Index page : \n" + __name__ + '\n|' + __name__.split('.')[0]

@main.route('/second')
def test():
    return render_template('hello.html',name = "Joe Duh")




if __name__ == '__main__':
    pass