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

from booktags.crawlers.base import BaseCrawler


# --------------------------------------------------------- common routines

def what():
    pass


class LibYlcCrawler(BaseCrawler):
    """
    Search 雲林縣公共圖書館	    http://library.ylccb.gov.tw/webpacIndex.jsp
    1. regular data
    2. marc
    """
    base_domain = "http://library.ylccb.gov.tw"
    search_domain = "https://search.books.com.tw"
    search_path = "/search/query/key/"
    protocol = "https:"

    def __init__(self):
        pass

    def search_isbn(self,isbn):
        pass

    def get_soup(self,url):
        pass



if __name__ == '__main__':
    pass
