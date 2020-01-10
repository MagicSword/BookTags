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

from booktags.crawlers.libylc.libylc_spider import LibYlcCrawler


# --------------------------------------------------------- common routines
class TestLibYlcCrawler(unittest.TestCase):

    def setUp(self):
        self.spider = LibYlcCrawler()

    def tearDown(self):
        self.spider = None

    # @unittest.skip("test search isbn")
    def test_search_isbn(self):
        isbn = "9789570810783"
        urls_ans = ['202757', '42281', '52904', '10641', '518923', '194353']

        urls_result = self.spider.search_isbn(isbn)

        self.assertEqual(urls_result, urls_ans)

    def test_get_soup(self):
        import bs4
        url = "http://library.ylccb.gov.tw/bookDetail.do?id=580659"
        soup_result = self.spider.get_soup(url)
        self.assertIsInstance(soup_result, bs4.BeautifulSoup)

    def test_fetch_blocks(self):
        import bs4

        isbn="9789864342815"
        ids=self.spider.search_isbn(isbn)
        block=self.spider.fetch_blocks(ids[0])

        fetch_result=block
        self.assertIsInstance(fetch_result["cover_block"], bs4.element.Tag)
        self.assertIsInstance(fetch_result["top_block"], bs4.BeautifulSoup)
        self.assertIsInstance(fetch_result["bot_block"], bs4.BeautifulSoup)


    def test_fetch_marc(self):
        self.fail()

    def test_parse_cover_block(self):
        cover_ans={'image': 'http://pic.eslite.com/Upload/Product/201802/m/636548259287033750.jpg'}
        isbn="9789864342815"
        ids=self.spider.search_isbn(isbn)
        block=self.spider.fetch_blocks(ids[0])
        cover_result=self.spider.parse_cover_block(block['cover_block'])

        self.assertEqual(cover_result, cover_ans)


    def test_parse_top_block(self):
        """

        :return:
        """
        top_ans={'name': '圖說演算法:使用Python:理解零負擔.採高CP值Python語言實作',
         'author': '吳燦銘,胡昭民著',
         'in_language': '中文',
         'isbn': '9789864342815',
         'book_edition': '初版',
         'publisher': '博碩文化',
         'location_created': '新北市汐止區',
         'summary': '內容簡介\n\n\n\n\n\n\n理解零負擔，採高 CP 值 Python 語言實作一本輕量級演算法，是您獲得程式設計新技能，提升自我價值的最好投資當「寫程式」納入必修課程的趨勢下，程式設計或設計APP已是大部分學生或社會人士必須具備的基礎能力。而演算法更是用來培養程式設計邏輯的基礎理論，也是有志從事資訊工作人員不得不重視的基礎課程。為了讓讀者能以容易理解的方式吸收演算法與基礎資料結構的相關知識，全書使用簡明的圖例介紹最常用演算法的概念，包括：分治法、遞迴法、貪心法、動態規劃法、疊代法、枚舉法、回溯法…等，並應用不同演算法延伸出重要資料結構，例如：陣列、鏈結串列、堆疊、佇列、樹狀結構、圖形、排序、搜尋、雜湊…等。同時搭配Python程式語言舉例實作，是您入門演算法的最佳首選。'
         }

        url = "http://library.ylccb.gov.tw/bookDetail.do?id=574061"
        isbn="9789864342815"
        ids=self.spider.search_isbn(isbn)
        block=self.spider.fetch_blocks(ids[0])
        top_result=self.spider.parse_top_block(block["top_block"])

        self.assertEqual(top_result, top_ans)

    def test_parse_bot_block(self):
        self.fail()

    def test_get_book(self):
        self.fail()

