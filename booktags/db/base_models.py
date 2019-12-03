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

import abc


# --------------------------------------------------------- common routines

# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, DateTime, String, Text, ForeignKey , Integer
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()
ID_LEN = 100
STR_LEN = 1024



# https://schema.org.cn/Thing.html
class ThingClass(Base):
    __tablename__ = "Thing"

    id = Column(String(ID_LEN), primary_key=True)
    name = Column(String(STR_LEN))
    url = Column(String(STR_LEN))
    image = Column(String(STR_LEN),nullable=True)
    category = Column(String(STR_LEN),nullable=True)
    description = Column(Text,nullable=True)

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

    author = Column(String(STR_LEN))
    translator = Column(String(STR_LEN),nullable=True)
    publisher = Column(String(STR_LEN))
    copyrightYear = Column(String(STR_LEN))
    abstract = Column(String(STR_LEN))
    inLanguage = Column(String(STR_LEN))
    genre = Column(String(STR_LEN))
    about = Column(String(STR_LEN))
    keywords = Column(String(STR_LEN))
    position = Column(String(STR_LEN))
    material = Column(String(STR_LEN)) # leather, wool , cotton ,  paper
    materialExtent = Column(String(STR_LEN))# The quantity of the materials being described or an expression of the physical space they occupy.


class BookClass(CreativeWorkClass):
    __tablename__ = "Book"

    bookEdition = Column(String(STR_LEN))# 1st,2nd,3th
    bookFormat =  Column(String(STR_LEN))# EBook,Hardcover,Paperback
    illustrator = Column(String(STR_LEN))
    isbn = Column(String(STR_LEN))
    numberOfPages = Column(String(STR_LEN))

class VideoGameClass(CreativeWorkClass):
    pass

class MovieClass(CreativeWorkClass):
    pass

class MusicRecordingClass(CreativeWorkClass):
    pass





if __name__ == '__main__':
    pass