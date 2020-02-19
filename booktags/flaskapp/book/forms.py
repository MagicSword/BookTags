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
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,DateField,IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms.widgets import TextArea
from wtforms import ValidationError
# from flask_pagedown.fields import PageDownField
from ..model.models import Role, User

# --------------------------------------------------------- common routines

class EditBookForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[Length(10, 13),DataRequired()])
    title_short = StringField('Short Title', validators=[Length(0, 64)])
    title = StringField('Title', validators=[Length(0, 100)])
    catalogue = StringField('Catalogue number', validators=[Length(0, 64)])
    cutter = StringField('Author number', validators=[Length(0, 64)])
    pub_year = StringField('Publish Year', validators=[Length(0, 64)])
    copy_info = StringField('Copy Info', validators=[Length(0, 64)])
    get_link = StringField('get_link', validators=[Length(0, 64)])
    note = StringField('Note', validators=[Length(0, 64)])
    reprint = StringField('Reprint', validators=[Length(0, 64)])
    removed = StringField('Removed', validators=[Length(0, 64)])
    keepsite = StringField('Keep site', validators=[Length(0, 64)])
    submit = SubmitField('Submit')

class HackmdMeta(FlaskForm):
    booksn = StringField('Books SN', validators=[Length(0, 64)])
    submit = SubmitField('Submit')
    body = StringField('body', widget=TextArea())


if __name__ == '__main__':
    pass