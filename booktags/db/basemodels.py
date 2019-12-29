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

    id = db.Column(db.String(ID_LEN), primary_key=True)
    name = db.Column(db.String(STR_LEN))
    url = db.Column(db.String(STR_LEN))
    image = db.Column(db.String(STR_LEN),nullable=True)
    alternateName = db.Column(db.String(STR_LEN),nullable=True)
    description = db.Column(db.Text,nullable=True)
    width = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    depth = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return "<{} : (id='{}',name='{}' )>".format(self.__class__.__name__,self.id,self.name)



class PersonClass(ThingClass):
    pass
    # __tablename__ = ""
    #
    # address
    # telephone
    # birthDate
    # birthPlace
    # children
    # parent
    # sibling
    # colleague
    # email
    # familyName
    # givenName
    # gender



class CreativeWorkClass(ThingClass):
    __tablename__ = "CreativeWork"

    author = db.Column(db.String(STR_LEN))
    translator = db.Column(db.String(STR_LEN),nullable=True)
    publisher = db.Column(db.String(STR_LEN))
    copyrightYear = db.Column(db.Datetime)
    abstract = db.Column(db.Text)
    about = db.Column(db.Text)
    locationCreated = db.Column(db.String(STR_LEN))
    contentRating = db.Column(db.String(STR_LEN))
    datePublished = db.Column(db.Datetime)
    inLanguage = db.Column(db.String(STR_LEN))
    genre = db.Column(db.String(STR_LEN))
    review = db.Column(db.Text)
    comment = db.Column(db.Text)
    translationOfWord = db.Column(db.String(STR_LEN))
    workTranslation = db.Column(db.String(STR_LEN))
    keywords = db.Column(db.String(STR_LEN))
    position = db.Column(db.String(STR_LEN)) # The position of an item in a series or sequence of items.
    material = db.Column(db.String(STR_LEN)) # leather, wool , cotton ,  paper
    materialExtent = db.Column(db.String(STR_LEN))# The quantity of the materials being described or an expression of the physical space they occupy.


class BookClass(CreativeWorkClass):
    __tablename__ = "Book"

    title = db.Column(db.String(STR_LEN))
    title_english = db.Column(db.String(STR_LEN))
    subtitle = db.Column(db.String(STR_LEN))
    isbn = db.Column(db.String(STR_LEN))
    illustrator = db.Column(db.String(STR_LEN))
    bookEdition = db.Column(db.String(STR_LEN))# 1st,2nd,3th
    bookFormat =  db.Column(db.String(STR_LEN))# EBook,Hardcover,Paperback
    numberOfPages = db.Column(db.Integer)
    price = db.Column(db.Integer)
    series = db.Column(db.String(STR_LEN))
    summary = db.Column(db.Text)
    summary = db.Column(db.Text)
    toc = db.Column(db.Text)
    category = db.Column(db.String(STR_LEN))

class StoreBookClass(BookClass):
    discount_price = db.Column(db.Integer)
    discountRate = db.Column(db.Float)
    discountDate = db.Column(db.Datetime)
    paperSize = db.Column(db.String(STR_LEN))
    printingColor = db.Column(db.String(STR_LEN))

class LibraryBookClass(BookClass):
    number_category = db.Column(db.String(STR_LEN))
    num_author = db.Column(db.String(STR_LEN))
    keepsite = db.Column(db.String(STR_LEN))
    number_copies = db.Column(db.Integer)


class VideoGameClass(CreativeWorkClass):
    pass

class MovieClass(CreativeWorkClass):
    pass

class MusicRecordingClass(CreativeWorkClass):
    pass

class StoreBookSchema(ma.ModelSchema):
    class Meta:
        model = StoreBookClass


class LibraryBookSchema(ma.TableSchema):
    class Meta:
        model = LibraryBookClass



if __name__ == '__main__':
    pass
