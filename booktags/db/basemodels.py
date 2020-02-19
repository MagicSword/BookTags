#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    example.py
    ~~~~~~~~~
    A simple command line application to run flask apps.
    :copyright: 2019 Miller
    :license: BSD-3-Clause

    :note:
    1. [SQLAlchemy Inheritance
](https://golden-note.readthedocs.io/zh/latest/python/sqlalchemy/inheritance.html)
        * Joined Table Inheritance
            * joined table
        * Single Table Inheritance
            * all class  in same table
        * Concrete Table Inheritance
            * bad
"""

# Known bugs that can't be fixed here:
#   - synopsis() cannot be prevented from clobbering existing
#     loaded modules.
#   - If the __file__ attribute on a module is a relative path and
#     the current directory is changed with os.chdir(), an incorrect
#     path will be displayed.

import bleach
from datetime import datetime, timedelta
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
    # CreativeWork
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
    review = db.Column(db.Text)   # long article
    comment = db.Column(db.Text)  # short message
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
    # bookstw_id = db.Column(db.Integer)
    # discount_price = db.Column(db.Integer)
    # discount_rate = db.Column(db.Float)
    # discount_date = db.Column(db.DateTime)
    # paper_size = db.Column(db.String(ID_LEN))
    # printing_color = db.Column(db.String(ID_LEN))
    # dimensions = db.Column(db.String(STR_LEN))

    # LibraryBook
    # libylc_id = db.Column(db.Integer)
    number_category = db.Column(db.String(ID_LEN))
    number_author = db.Column(db.String(ID_LEN))
    keepsite = db.Column(db.String(ID_LEN)) # shelf ?
    number_copies = db.Column(db.Integer)
    marc_blob = db.Column(db.BLOB)
    # misc
    bookmain_id = db.Column(db.Integer, db.ForeignKey('bookmain.id'))
    hidden = db.Column(db.Boolean, default=0)
    # from goodread
    # MY ACTIVITY: read process, read status
    reading_processs= db.Column(db.Integer)  # current page
    rating_stars= db.Column(db.Integer)  # my rating: 5/5 star, int
    # shelve_id = db.relationship('Shelve',
    #                             secondary=book_tag,
    #                             backref=db.backref('shelves', lazy='dynamic'),
    #                             lazy='dynamic')

    # myAttribute
    # total
    # toRead
    # currentlyReading
    # read
    # reference
    # to_give_up

    booktable_type = db.Column(db.String(ID_LEN))

    __mapper_args__ = {
        'polymorphic_identity': 'books',
        'polymorphic_on': booktable_type
    }


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


    def __repr__(self):
        return "<{} : (id='{}',name='{}')>".format(self.__class__.__name__,self.id,self.name)


db.event.listen(Book.summary, 'set', Book.on_changed_summary)
db.event.listen(Book.about_author, 'set', Book.on_changed_about_author)
db.event.listen(Book.toc, 'set', Book.on_changed_toc)


class BooksTwBook(Book):
    """ books.com.tw Book class

    """
    __tablename__ = "bookstw_books"
    # __table_args__ = {'extend_existing': True}


    id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    discount_price = db.Column(db.Integer)
    discount_rate = db.Column(db.Float)
    discount_date = db.Column(db.DateTime)
    paper_size = db.Column(db.String(ID_LEN))
    printing_color = db.Column(db.String(ID_LEN))
    dimensions = db.Column(db.String(STR_LEN))  # 規格 string

    __mapper_args__ = {
        'polymorphic_identity': 'bookstw_books'
    }

class LibYlcBook(Book):
    """ library.ylccb.gov.tw Book class

    """
    __tablename__ = "libylc_books"
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    number_category = db.Column(db.String(ID_LEN))
    number_author = db.Column(db.String(ID_LEN))
    keepsite = db.Column(db.String(ID_LEN))
    number_copies = db.Column(db.Integer)  # 館藏數量

    __mapper_args__ = {
        'polymorphic_identity': 'libylc_books'
    }

    def __repr__(self):
        return "<{} : (id = '{}', name = '{}' )>".format(self.__class__.__name__,self.id,self.name)


class MyBook(Book):
    """ library.ylccb.gov.tw Book class

    """
    __tablename__ = "my_books"
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    number_category = db.Column(db.String(ID_LEN))
    number_author = db.Column(db.String(ID_LEN))
    keepsite = db.Column(db.String(ID_LEN))
    number_copies = db.Column(db.Integer)  # 館藏數量

    __mapper_args__ = {
        'polymorphic_identity': 'my_books'
    }

    def __repr__(self):
        return "<{} : (id = '{}', name = '{}' )>".format(self.__class__.__name__,self.id,self.name)

# class VideoGameClass(CreativeWork):
#     pass
#
# class MovieClass(CreativeWork):
#     pass
#
# class MusicRecordingClass(CreativeWork):
#     pass


class MARCClass(db.Model):
    """ MARC
    MARC type: CMARC,MARC21

    """
    __tablename__ = "marc"


    id = db.Column(db.String(ID_LEN), primary_key=True)
    isbn = db.Column(db.String(ID_LEN), unique=True, index=True)
    name = db.Column(db.String(STR_LEN))
    author = db.Column(db.String(STR_LEN))

    image_url = db.Column(db.String(STR_LEN))
    descritption = db.Column(db.TEXT, nullable=True)
    # 預設 CMARCv3, JSON 也是 CMARCv3 2007 版
    marc = db.Column(db.BLOB, nullable=True)
    json = db.Column(db.JSON, nullable=True)
    xml = db.Column(db.BLOB, nullable=True)


    def save_marc(self,filepath):
        if self.marc is None:
            return False
        else:
            with open(filepath,'wb') as fd:
                fd.write(filepath)

    def save_json(self,filepath):
        import json
        if self.json is None:
            self.marcjson()
        else:
            with open(filepath,'w') as fd:
                json.dump(self.json, fd)

    def load_json(self):
        pass

    def load_marc(self,fobj):
        self.marc=fobj

    def marcjson(self):
        pass

    def marcxml(self):
        pass

    def __repr__(self):
        return "<{} : (id = '{}', name = '{}' )>".format(self.__class__.__name__,self.id,self.name)




class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    borrow_timestamp = db.Column(db.DateTime, default=datetime.now())
    return_timestamp = db.Column(db.DateTime, default=datetime.now())
    returned = db.Column(db.Boolean, default=0)

    def __init__(self, user, book):
        self.user = user
        self.book = book
        self.borrow_timestamp = datetime.now()
        self.return_timestamp = datetime.now() + timedelta(days=30)
        self.returned = 0

    def __repr__(self):
        return u'<%r - %r>' % (self.user.name, self.book.title)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    comment = db.Column(db.String(1024))
    create_timestamp = db.Column(db.DateTime, default=datetime.now())
    edit_timestamp = db.Column(db.DateTime, default=datetime.now())
    deleted = db.Column(db.Boolean, default=0)

    def __init__(self, book, user, comment):
        self.user = user
        self.book = book
        self.comment = comment
        self.create_timestamp = datetime.now()
        self.edit_timestamp = self.create_timestamp
        self.deleted = 0


book_tag = db.Table('books_tags',
                    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                    )


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    books = db.relationship('Book',
                            secondary=book_tag,
                            backref=db.backref('books', lazy='dynamic'),
                            lazy='dynamic')

    def __repr__(self):
        return u'<Tags %s>' % self.name


# class Shelve(db.Model):
#     __tablename__ = 'shelves'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     books = db.relationship('Book',
#                             secondary=book_tag,
#                             backref=db.backref('books', lazy='dynamic'),
#                             lazy='dynamic')
#
#     def __repr__(self):
#         return u'<ShelvesTag %s>' % self.name


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


