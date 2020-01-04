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

from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from .flaskapp import db
from .flaskapp.model.models import User, Post
from booktags.db.basemodels import Book
# --------------------------------------------------------- common routines

def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def posts(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=fake.text(),
                 timestamp=fake.past_date(),
                 author=u)
        db.session.add(p)
    db.session.commit()


def books(count=100):
    fake = Faker(['zh_TW'])
    i = 0
    while i < count:
        b = Book(name=fake.text(50),
                 url=fake.uri(),
                 image=fake.image_url(),
                 width=17.0,
                 height=23.0,
                 depth=4.25,
                 author=fake.name(),
                 translator=fake.name(),
                 publisher=fake.company(),
                 date_published=fake.past_date(),
                 in_language=fake.language_code(),
                 location_created=fake.local_latlng()[4],
                 isbn=fake.isbn13(separator=''),
                 number_pages=randint(200,1500),
                 price=randint(100,1000),
                 summary=fake.text(),
                 about_author=fake.text(),
                 toc=fake.text(),
                 series=fake.text(5),
                 category=fake.text(10)
                    )
        db.session.add(b)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()