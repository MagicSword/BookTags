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

from sqlalchemy import Boolean, Column, DateTime, String, Text, ForeignKey, VARBINARY,JSON,NVARCHAR
from sqlalchemy.ext.declarative import declarative_base
#from .base_models import BookClass

Base = declarative_base()
ID_LEN = 100
STR_LEN = 1024




class MARCClass(Base):
    __tablename__ = "marc"

    id = Column(String(ID_LEN), primary_key=True)
    name = Column(String(STR_LEN))
    image_url = Column(String(STR_LEN))
    descritption = Column(NVARCHAR(), nullable=True)
    marc = Column(VARBINARY(), nullable=True)
    marc_json = Column(JSON(), nullable=True)

    def __repr__(self):
        return "<{} : (id = '{}', name = '{}' )>".format(self.__class__.__name__,self.id,self.name)










if __name__ == '__main__':
    pass