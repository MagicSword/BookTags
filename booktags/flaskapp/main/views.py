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

from datetime import datetime

from . import main
from flask import render_template
from .forms import SigninForm, SignupForm


from .navbar import nav

# --------------------------------------------------------- common routines


@main.route('/')
@main.route('/index')
def index():
    print(__name__)
    print(__name__.split('.')[0])
    msg = "Flask app Index page(__name__) : \n" + __name__
    return render_template('index.html',message=msg,current_time=datetime.utcnow())

@main.route('/signin', methods=['GET','POST'])
def signin():
    username = None
    form = SigninForm()
    if form.validate_on_submit():
        username=form.username.data
        passowrd=form.password.data
        form.username.data=''
        form.password.data=''
        return render_template('signin.html',form=form,username=username,password=password)

@main.route('/signup')
def signup():
    pass

@main.route('/user/<username>')
def user(username):
    return render_template('user.html',name=username)

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def all_exception_handler(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    pass