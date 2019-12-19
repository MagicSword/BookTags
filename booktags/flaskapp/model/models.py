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

from .. import db
# --------------------------------------------------------- common routines

#model = SQLAlchemy()

Boolean_LEN = 10
ID_LEN = 50
STR_LEN = 200

class BookMain(db.Model):
    __tablename__ = "book_main"

    id = db.Column(db.String(ID_LEN), primary_key=True)
    isbn = db.Column(db.String(ID_LEN), index=True)
    title_short = db.Column(db.String(ID_LEN))
    title = db.Column(db.String(STR_LEN))
    catalogue = db.Column(db.String(ID_LEN))
    cutter = db.Column(db.String(ID_LEN))
    pub_year = db.Column(db.String(ID_LEN))
    copy_info = db.Column(db.String(ID_LEN), nullable=True)
    get_link = db.Column(db.String(Boolean_LEN), nullable=True)
    note = db.Column(db.String(STR_LEN), nullable=True)
    reprint = db.Column(db.String(Boolean_LEN), nullable=True)
    removed = db.Column(db.String(Boolean_LEN), nullable=True)
    keepsite = db.Column(db.String(ID_LEN), nullable=True)

    # marc_json = Column(JSON(), nullable=True)

    def __repr__(self):
        return "<{} : (id = '{}', isbn = '{}' )>".format(self.__class__.__name__,self.id,self.isbn)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username



if __name__ == '__main__':
    pass