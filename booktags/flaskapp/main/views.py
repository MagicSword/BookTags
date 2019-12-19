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

from flask import render_template,flash, session, redirect, url_for,current_app

from . import main
from .forms import SigninForm, SignupForm, NameForm
from ..model.models import User
from .. import db
from ..email import send_email
from .navbar import nav

# --------------------------------------------------------- common routines



@main.route('/', methods=['GET', 'POST'])
def index():
    flash("Name of file: {}".format(__name__), 'danger')
    msg = "Hello"
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['PROJECT_ADMIN']:
                send_email(current_app.config['PROJECT_ADMIN'], f'New User -{user.username}',
                           'mail/new_user', user=user)

        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           message=msg, current_time=datetime.utcnow(),
                           known=session.get('known', False))


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
    username= None
    form = SignupForm()

@main.route('/user/<username>')
def user(username):
    return render_template('user.html',name=username)




if __name__ == '__main__':
    pass