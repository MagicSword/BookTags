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


import re
import time
import unittest

import pandas as pd
from datetime import datetime

from booktags.crawlers.bookstw.bookstw_spider import BooksTwCrawler


# --------------------------------------------------------- common routines
class TestBooksTwCrawler(unittest.TestCase):
    def setUp(self):
        # self.app = create_app('testing')
        # self.app_context = self.app.app_context()
        # self.app_context.push()
        # db.create_all()
        # Role.insert_roles()
        # self.client = self.app.test_client(use_cookies=True)
        self.base_domain = "https://www.books.com.tw"
        self.search_domain = "https://search.books.com.tw"
        self.search_path = "/search/query/key/"
        self.protocol = "https:"

        self.spider = BooksTwCrawler()

        filepath = "file:///E:/_Documents/GitHub/PyCharm_Workspace/BookTags/tmp/bookshelf_main.csv"
        self.df = pd.read_csv(filepath)

    def tearDown(self):
        # db.session.remove()
        # db.drop_all()
        # self.app_context.pop()
        self.spider = None

    # def test_home_page(self):
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('Stranger' in response.get_data(as_text=True))

    # @unittest.skip("test search isbn")
    def test_search_isbn(self):
        ans_ids = self.spider.search_isbn('9789578423886')
        result_ids = set()
        result_ids.update(['0010823875', 'E050048572'])

        self.assertEqual(ans_ids, result_ids)

    # @unittest.skip("test get_blocks")
    def test_get_blocks(self):
        ids = ["0010834816", "CN11708291"]
        names = ["Python 技術者們：練功！老手帶路教你精通正宗 Python 程式", "盜墓筆記十年"]

        for idx, name in zip(ids, names):
            print(f"id:{id}\n name:{name}")

            url = f"{self.base_domain}/products/{idx}"
            soup = self.spider.get_soup(url)
            block = self.spider.get_blocks(soup)

            print(type(block))
            time.sleep(1)

            self.assertEqual(block['title_block'].h1.string, name)

    # @unittest.skip("test parse head block")
    def test_parse_head_block(self):
        idx = "0010834816"
        url = f"{self.base_domain}/products/{idx}"
        soup = self.spider.get_soup(url)
        block = self.spider.get_blocks(soup)

        head_result = self.spider.parse_head_block(block['head_block'])
        head_ans = {
            'name': "Python 技術者們：練功！老手帶路教你精通正宗 Python 程式",
            'image': "https://www.books.com.tw/img/001/083/48/0010834816.jpg",
            'url': "http://www.books.com.tw/products/0010834816"
        }
        self.assertEqual(head_result, head_ans)

    # @unittest.skip("test parse title block")
    def test_parse_title_block(self):
        idx = "0010834816"
        url = f"{self.base_domain}/products/{idx}"
        soup = self.spider.get_soup(url)
        block = self.spider.get_blocks(soup)

        title_result = self.spider.parse_title_block(block['title_block'])
        title_ans = {
            'title': "Python 技術者們",
            'subtitle': "練功！老手帶路教你精通正宗 Python 程式",
            'title_english': "The Quick Python Book Third Edition"
        }
        self.assertEqual(title_result, title_ans)

    # @unittest.skip("test pub block")
    def test_parse_pub_block(self):
        idx = "0010794173"
        url = f"{self.base_domain}/products/{idx}"
        soup = self.spider.get_soup(url)
        block = self.spider.get_blocks(soup)

        pub_result = self.spider.parse_pub_block(block['pub_block'])
        pub_ans = {
            "author": "傑森‧布倫南",
            "author_origin" : "Jason Brennan",
            "publisher": "聯經出版公司",
            "date_published": datetime.strptime("2018/08/07", "%Y/%m/%d"),
            'translator': '劉維人',
            "in_language": "繁體中文"
        }
        self.assertEqual(pub_result, pub_ans)

    # @unittest.skip("test price block")
    def test_parse_price_block(self):
        idx = "0010831978"
        url = f"{self.base_domain}/products/{idx}"
        soup = self.spider.get_soup(url)
        block = self.spider.get_blocks(soup)

        price_result = self.spider.parse_price_block(block['price_block'])
        price_ans = {
            "price": 1000,
            "discount_price": 660,
            "discount_rate": 0.66,
            "discount_date": datetime.strptime("2020年01月05日止", '%Y年%m月%d日止')
        }
        self.assertEqual(price_result, price_ans)

    # @unittest.skip("test parse detail block")
    def test_parse_detail_block(self):
        idx = "0010843006"
        url = f"{self.base_domain}/products/{idx}"
        soup = self.spider.get_soup(url)
        block = self.spider.get_blocks(soup)

        detail_result = self.spider.parse_detail_block(block['detail_block'])

        detail_ans = {
            "isbn": "9789865501051",
            "series": "",
            "location_created": "台灣",
            'book_format': '平裝',
            'number_pages': 384,
            'dimensions': '17 x 23 x 1.9 cm',
            'content_rating': '普通級',
            'printing_color': '單色印刷',
            'book_edition': '初版',
            'width': 17.0,
            'height': 23.0,
            'depth': 1.9}

        self.assertEqual(detail_result, detail_ans)

    # @unittest.skip("test parse specification")
    def test_parse_specification(self):
        spe = "規格：平裝 / 256頁 / 17 x 23 x 1.28 cm / 普通級 / 雙色印刷 / 初版"
        spe_result = self.spider.parse_specification(spe)
        spe_ans = {
            'book_format': '平裝',
            'number_pages': '256頁',
            'dimensions': '17 x 23 x 1.28 cm',
            'content_rating': '普通級',
            'printing_color': '雙色印刷',
            'book_edition': '初版',
            'width': '17',
            'height': '23',
            'depth': '1.28'}
        self.assertEqual(spe_result, spe_ans)

    # @unittest.skip("test parse sort block")
    def test_parse_sort_block(self):
        idx = "0010843696"
        url = f"{self.base_domain}/products/{idx}"
        soup = self.spider.get_soup(url)
        block = self.spider.get_blocks(soup)

        sort_result = self.spider.parse_sort_block(block['sort_block'])
        sort_ans = "|商業理財> 職場工作術> 求職／履歷面試|商業理財> 成功法> 生涯規劃"
        self.assertEqual(sort_result, sort_ans)

    # @unittest.skip("test get contents")
    def test_get_contents(self):
        idx = "0010843696"
        url = f"{self.base_domain}/products/{idx}"
        soup = self.spider.get_soup(url)
        block = self.spider.get_blocks(soup)

    # @unittest.skip("test get book")
    def test_get_book(self):
        idx="0010843696"
        book_result = self.spider.get_book(idx)
        book_ans = {
            'name': '2030轉職地圖：成為未來10年不被淘汰的國際人才',
            'url': 'http://www.books.com.tw/products/0010843696',
            'image':'https://www.books.com.tw/img/001/084/36/0010843696.jpg',
            'author':'Sandy Su（蘇盈如）',
            'publisher':'遠流',
            'in_language' : '繁體中文',
            'price':360
        }
        self.assertEqual(book_ans['name'] , book_result['name'])
        self.assertEqual(book_ans['url'], book_result['url'])
        self.assertEqual(book_ans['image'], book_result['image'])
        self.assertEqual(book_ans['author'], book_result['author'])
        self.assertEqual(book_ans['publisher'], book_result['publisher'])
        self.assertEqual(book_ans['in_language'], book_result['in_language'])
        self.assertEqual(book_ans['price'], book_result['price'])


if __name__ == '__main__':
    unittest.main()



