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

import re
import threading
import time
import unittest

from booktags.flaskapp import create_app, db
from booktags import fake

from booktags.crawlers.bookstw.bookstw_crawler import BooksTwCrawler
from ward import each, fixture, test,expect



@fixture
def bookstw_api():
    return BooksTwCrawler()

@test("bookstw.search_from_isbn from isbn returns bookstw_id list")
def test_search_from_isbn():
    """
    :param: isbn
    :return: list id
    9789579094382
    ['0010823875','E050048572']
    """
    spider = bookstw_api()
    spider.search_isbn('9789578423886')
    result_id = ['0010823875','E050048572']
    expect(spider.bookstw_result_id).equals(result_id)

def test_get_product():
    """
    :param:
    :return:
    """


@test("bookstw.get_product returns the correct book given an ISBN")
def _(
   api=bookstw_api,
   isbn=each("9789863125914", "9787559637949", "9781947194373"),
   name=each("Python 技術者們", "盜墓筆記十年", "A Scandal in Japan")):
   book: BooksTwCrawler = api.get_product(isbn)
   expect(book.name).equals(name)


if __name__ == '__main__':
    pass