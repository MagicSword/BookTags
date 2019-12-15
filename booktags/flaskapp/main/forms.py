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

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import DataRequired,EqualTo,Email,InputRequired


# --------------------------------------------------------- common routines

class SigninForm(FlaskForm):
    """

    """
    username=StringField("Username or email address",validators=[InputRequired()])
    password=PasswordField("Password",validators=[InputRequired()])
    signin=SubmitField("Sign in")

class SignupForm(FlaskForm):
    """

    """
    username=StringField("Username",[InputRequired()])
    email=StringField("Email",[InputRequired(), Email])
    password=PasswordField("Password",[InputRequired(), EqualTo('confirm',message="Passwords must match")])
    confirm=PasswordField("Confirm Password",[InputRequired()])
    signup=SubmitField("Sign up")




if __name__ == '__main__':
    pass