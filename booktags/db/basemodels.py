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

from ..flaskapp import db
from ..flaskapp import ma


# --------------------------------------------------------- common routines

ID_LEN = 100
STR_LEN = 1024

# https://schema.org.cn/Thing.html
class ThingClass(db.Model):
    __tablename__ = "Thing"
    __table_args__ = {'extend_existing': True}


    id = db.Column(db.String(ID_LEN), primary_key=True)
    name = db.Column(db.String(STR_LEN))
    url = db.Column(db.String(STR_LEN))
    image = db.Column(db.String(STR_LEN),nullable=True)
    alternate_name = db.Column(db.String(STR_LEN),nullable=True)
    description = db.Column(db.Text,nullable=True)
    width = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    depth = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Thing'
    }

    def __repr__(self):
        return "<{} : (id='{}',name='{}' )>".format(self.__class__.__name__,self.id,self.name)



# class PersonClass(ThingClass):
#     pass
#     __tablename__ = ""
#
#     address
#     telephone
#     birthDate
#     birthPlace
#     children
#     parent
#     sibling
#     colleague
#     email
#     familyName
#     givenName
#     gender



class CreativeWorkClass(ThingClass):
    __tablename__ = "CreativeWork"
    # __table_args__ = {'extend_existing': True}


    author = db.Column(db.String(STR_LEN))
    translator = db.Column(db.String(STR_LEN),nullable=True)
    publisher = db.Column(db.String(STR_LEN))
    copyright_year = db.Column(db.DateTime)
    abstract = db.Column(db.Text)
    about = db.Column(db.Text)
    location_created = db.Column(db.String(STR_LEN))
    content_rating = db.Column(db.String(STR_LEN))
    date_published = db.Column(db.DateTime)
    in_language = db.Column(db.String(STR_LEN))
    genre = db.Column(db.String(STR_LEN))
    review = db.Column(db.Text)
    comment = db.Column(db.Text)
    translation_Work = db.Column(db.String(STR_LEN))
    work_translation = db.Column(db.String(STR_LEN))
    keywords = db.Column(db.String(STR_LEN))
    position = db.Column(db.String(STR_LEN)) # The position of an item in a series or sequence of items.
    material = db.Column(db.String(STR_LEN)) # leather, wool , cotton ,  paper
    material_extent = db.Column(db.String(STR_LEN))# The quantity of the materials being described or an expression of the physical space they occupy.

    __mapper_args__ = {
        'polymorphic_identity': 'CreativeWord'
    }


class BookClass(CreativeWorkClass):
    __tablename__ = "Book"
    # __table_args__ = {'extend_existing': True}


    title = db.Column(db.String(STR_LEN))
    title_english = db.Column(db.String(STR_LEN))
    subtitle = db.Column(db.String(STR_LEN))
    isbn = db.Column(db.String(STR_LEN))
    illustrator = db.Column(db.String(STR_LEN))
    book_edition = db.Column(db.String(STR_LEN))# 1st,2nd,3th
    book_format =  db.Column(db.String(STR_LEN))# EBook,Hardcover,Paperback
    number_pages = db.Column(db.Integer)
    price = db.Column(db.Integer)
    series = db.Column(db.String(STR_LEN))
    summary = db.Column(db.Text)
    summary_author = db.Column(db.Text)
    toc = db.Column(db.Text)
    category = db.Column(db.String(STR_LEN))

    __mapper_args__ = {
        'polymorphic_identity': 'Book'
    }

class StoreBookClass(BookClass):
    __tablename__ = "StoreBook"
    # __table_args__ = {'extend_existing': True}

    discount_price = db.Column(db.Integer)
    discount_rate = db.Column(db.Float)
    discount_date = db.Column(db.DateTime)
    paper_size = db.Column(db.String(STR_LEN))
    printing_color = db.Column(db.String(STR_LEN))

    __mapper_args__ = {
        'polymorphic_identity': 'StoreBook'
    }

class LibraryBookClass(BookClass):
    __tablename__ = "LibraryBook"
    # __table_args__ = {'extend_existing': True}

    number_category = db.Column(db.String(STR_LEN))
    num_author = db.Column(db.String(STR_LEN))
    keepsite = db.Column(db.String(STR_LEN))
    number_copies = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'LibraryBook'
    }


# class VideoGameClass(CreativeWorkClass):
#     pass
#
# class MovieClass(CreativeWorkClass):
#     pass
#
# class MusicRecordingClass(CreativeWorkClass):
#     pass


# class MARCClass(db.Model):
#     __tablename__ = "marc"
#
#     id = db.Column(db.String(ID_LEN), primary_key=True)
#     name = db.Column(db.String(STR_LEN))
#     image_url = db.Column(db.String(STR_LEN))
#     descritption = db.Column(db.NVARCHAR(), nullable=True)
#     marc = db.Column(db.VARBINARY(), nullable=True)
#     marc_json = db.Column(db.JSON(), nullable=True)
#
#     def __repr__(self):
#         return "<{} : (id = '{}', name = '{}' )>".format(self.__class__.__name__,self.id,self.name)

######   Marshmallow

class StoreBookSchema(ma.ModelSchema):
    class Meta:
        model = StoreBookClass


class LibraryBookSchema(ma.TableSchema):
    class Meta:
        model = LibraryBookClass





if __name__ == '__main__':
    pass
