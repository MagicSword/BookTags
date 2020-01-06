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

import bleach
from datetime import datetime
from markdown import markdown



from ..flaskapp import db
from ..flaskapp import ma


# --------------------------------------------------------- common routines

ID_LEN = 100
STR_LEN = 1024

# https://schema.org.cn/Thing.html
# class Thing(db.Model):
#     __tablename__ = "thing_class"
#     __table_args__ = {'extend_existing': True}
#
#     id = db.Column(db.String(ID_LEN), primary_key=True)
#     name = db.Column(db.String(STR_LEN))
#     url = db.Column(db.String(STR_LEN))
#     image = db.Column(db.String(STR_LEN),nullable=True)
#     alternate_name = db.Column(db.String(STR_LEN),nullable=True)
#     description = db.Column(db.Text,nullable=True)
#     width = db.Column(db.Float, nullable=True)
#     height = db.Column(db.Float, nullable=True)
#     depth = db.Column(db.Float, nullable=True)
#     weight = db.Column(db.Float, nullable=True)
#
#     __mapper_args__ = {
#         'polymorphic_identity': 'thing_class'
#     }
#
#     def __repr__(self):
#         return "<{} : (id='{}',name='{}')>".format(self.__class__.__name__,self.id,self.name)



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



# class CreativeWork(Thing):
#     __tablename__ = "creative_work"
#     # __table_args__ = {'extend_existing': True}
#
#
#     author = db.Column(db.String(STR_LEN))
#     translator = db.Column(db.String(STR_LEN),nullable=True)
#     publisher = db.Column(db.String(STR_LEN))
#     copyright_year = db.Column(db.DateTime)
#     abstract = db.Column(db.Text)
#     about = db.Column(db.Text)
#     location_created = db.Column(db.String(STR_LEN))
#     content_rating = db.Column(db.String(STR_LEN))
#     date_published = db.Column(db.DateTime)
#     in_language = db.Column(db.String(ID_LEN))
#     genre = db.Column(db.String(STR_LEN))
#     review = db.Column(db.Text)
#     comment = db.Column(db.Text)
#     translation_Work = db.Column(db.String(STR_LEN))
#     work_translation = db.Column(db.String(STR_LEN))
#     keywords = db.Column(db.String(STR_LEN))
#     position = db.Column(db.String(STR_LEN)) # The position of an item in a series or sequence of items.
#     material = db.Column(db.String(STR_LEN)) # leather, wool , cotton ,  paper
#     material_extent = db.Column(db.String(STR_LEN))# The quantity of the materials being described or an expression of the physical space they occupy.
#
#     __mapper_args__ = {
#         'polymorphic_identity': 'creative_work'
#     }


class Book(db.Model):
    __tablename__ = "books"
    # __table_args__ = {'extend_existing': True}
    # Thing
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(STR_LEN))
    url = db.Column(db.String(STR_LEN))
    image = db.Column(db.String(STR_LEN),nullable=True)
    alternate_name = db.Column(db.String(STR_LEN),nullable=True)
    description = db.Column(db.Text,nullable=True)
    width = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    depth = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    # creativeWork
    author = db.Column(db.String(STR_LEN))
    author_origin = db.Column(db.String(STR_LEN))
    translator = db.Column(db.String(STR_LEN),nullable=True)
    publisher = db.Column(db.String(STR_LEN))
    copyright_year = db.Column(db.DateTime)
    abstract = db.Column(db.Text)
    about = db.Column(db.Text)
    location_created = db.Column(db.String(STR_LEN))
    content_rating = db.Column(db.String(STR_LEN))
    date_published = db.Column(db.DateTime)
    in_language = db.Column(db.String(ID_LEN))
    genre = db.Column(db.String(STR_LEN))
    review = db.Column(db.Text)
    comment = db.Column(db.Text)
    translation_Work = db.Column(db.String(STR_LEN))
    work_translation = db.Column(db.String(STR_LEN))
    keywords = db.Column(db.String(STR_LEN))
    position = db.Column(db.String(STR_LEN)) # The position of an item in a series or sequence of items.
    material = db.Column(db.String(STR_LEN)) # leather, wool , cotton ,  paper
    material_extent = db.Column(db.String(STR_LEN))# The quantity of the materials being described or an expression of the physical space they occupy.
    # Book
    title = db.Column(db.String(STR_LEN))
    title_english = db.Column(db.String(STR_LEN))
    subtitle = db.Column(db.String(STR_LEN))
    isbn = db.Column(db.String(ID_LEN), unique=True, index=True)
    illustrator = db.Column(db.String(STR_LEN))
    book_edition = db.Column(db.String(ID_LEN))# 1st,2nd,3th
    book_format =  db.Column(db.String(STR_LEN))# EBook,Hardcover,Paperback
    number_pages = db.Column(db.Integer)
    price = db.Column(db.Integer)
    series = db.Column(db.String(STR_LEN))
    summary = db.Column(db.Text)
    summary_html = db.Column(db.Text)
    about_author = db.Column(db.Text)
    about_author_html = db.Column(db.Text)
    toc = db.Column(db.Text)
    toc_html = db.Column(db.Text)
    preface = db.Column(db.Text)
    category = db.Column(db.String(STR_LEN))
    # StoreBook
    discount_price = db.Column(db.Integer)
    discount_rate = db.Column(db.Float)
    discount_date = db.Column(db.DateTime)
    paper_size = db.Column(db.String(ID_LEN))
    printing_color = db.Column(db.String(ID_LEN))
    dimensions = db.Column(db.String(STR_LEN))

    # LibraryBook
    number_category = db.Column(db.String(ID_LEN))
    num_author = db.Column(db.String(ID_LEN))
    keepsite = db.Column(db.String(ID_LEN))
    number_copies = db.Column(db.Integer)
    # misc
    bookmain_id = db.Column(db.Integer, db.ForeignKey('bookmain.id'))


    __mapper_args__ = {
        'polymorphic_identity': 'books'
    }

    def __repr__(self):
        return "<{} : (id='{}',name='{}')>".format(self.__class__.__name__,self.id,self.name)

    @staticmethod
    def on_changed_summary(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.summary_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    @staticmethod
    def on_changed_about_author(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.about_author_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    @staticmethod
    def on_changed_toc(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.toc_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def add_book(self):
        db.session.add(self)
        db.session.commit()

    def delete_book(self):
        db.session.delete(self)
        db.session.commit()

    def update_book(self):
        db.session.commit()

    @classmethod
    def get_all_book(cls):
        return cls.query.all()

    @classmethod
    def get_book_byisbn(cls, isbn):
        return cls.query.filter_by(isbn=isbn).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.coommit()



# class StoreBook(Book):
#     __tablename__ = "storebook"
#     # __table_args__ = {'extend_existing': True}
#
#     discount_price = db.Column(db.Integer)
#     discount_rate = db.Column(db.Float)
#     discount_date = db.Column(db.DateTime)
#     paper_size = db.Column(db.String(ID_LEN))
#     printing_color = db.Column(db.String(ID_LEN))
#
#     __mapper_args__ = {
#         'polymorphic_identity': 'storebook'
#     }
#
# class LibraryBook(Book):
#     __tablename__ = "librarybook"
#     # __table_args__ = {'extend_existing': True}
#
#     number_category = db.Column(db.String(ID_LEN))
#     num_author = db.Column(db.String(ID_LEN))
#     keepsite = db.Column(db.String(ID_LEN))
#     number_copies = db.Column(db.Integer)
#
#     __mapper_args__ = {
#         'polymorphic_identity': 'librarybook'
#     }


# class VideoGameClass(CreativeWork):
#     pass
#
# class MovieClass(CreativeWork):
#     pass
#
# class MusicRecordingClass(CreativeWork):
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

class BookSchema(ma.ModelSchema):
    class Meta:
        model = Book


# class StoreBookSchema(ma.ModelSchema):
#     class Meta:
#         model = StoreBookClass
#
#
# class LibraryBookSchema(ma.TableSchema):
#     class Meta:
#         model = LibraryBookClass





if __name__ == '__main__':
    pass
