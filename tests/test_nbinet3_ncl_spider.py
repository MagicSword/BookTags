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

import unittest
from unittest import TestCase

from booktags.crawlers.nbinet3_ncl.nbinet3_ncl_spider import Nbinet3NlcCrawler


# --------------------------------------------------------- common routines
class TestNbinet3NlcCrawler(unittest.TestCase):

    def setUp(self):
        self.spider = Nbinet3NlcCrawler()

    def tearDown(self):
        self.spider = None

    # @unittest.skip("test search isbn")
    def test_search_isbn(self):
        isbn = "9789867778819"

        urls_ans = [
            "/search~S10*cht?/i9789867778819/i9789867778819/1%2C1%2C6%2CE/frameset&FF=i9789867778819&1%2C%2C6",
            "/search~S10*cht?/i9789867778819/i9789867778819/1%2C1%2C6%2CE/frameset&FF=i9789867778819&2%2C%2C6",
            "/search~S10*cht?/i9789867778819/i9789867778819/1%2C1%2C6%2CE/frameset&FF=i9789867778819&3%2C%2C6",
            "/search~S10*cht?/i9789867778819/i9789867778819/1%2C1%2C6%2CE/frameset&FF=i9789867778819&4%2C%2C6",
            "/search~S10*cht?/i9789867778819/i9789867778819/1%2C1%2C6%2CE/frameset&FF=i9789867778819&5%2C%2C6",
            "/search~S10*cht?/i9789867778819/i9789867778819/1%2C1%2C6%2CE/frameset&FF=i9789867778819&6%2C%2C6"
        ]
        urls_resust = self.spider.search_isbn(isbn)

        self.assertEqual(urls_resust, urls_ans)

    def test_parse_mid_block(self):
        """

        :return:
        """
        mid_ans = {'callnum': '312.32P97', 'author': '4423', 'year': '2016'}
        url = "http://nbinet3.ncl.edu.tw/search~S10*cht?/tpython3/tpython3/1%2C7%2C18%2CE/frameset&FF=tpython3++++507{21402c}{215746}04{213f7a}{213330}&1%2C%2C4"
        soup = self.spider.get_soup(url)
        block = self.spider.get_blocks(soup)
        mid_block = block['mid_block']
        mid_result = self.spider.parse_mid_block(mid_block)

        self.assertEqual(mid_result, mid_ans)


    def test_get_book(self):
        book_ans={
            'callnum': '312.32P97',
            'author': '4423',
            'year': '2016'
        }
        url = "http://nbinet3.ncl.edu.tw/search~S10*cht?/tpython3/tpython3/1%2C7%2C18%2CE/frameset&FF=tpython3++++507{21402c}{215746}04{213f7a}{213330}&1%2C%2C4"

        book_result=self.spider.get_book(url)

        self.assertEqual(book_result['callnum'], book_ans['callnum'])
        self.assertEqual(book_result['author'], book_ans['author'])
        self.assertEqual(book_result['year'], book_ans['year'])
