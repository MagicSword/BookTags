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
import re


from booktags.crawlers.bookstw.bookstw_crawler import BooksTwCrawler
# --------------------------------------------------------- common routines

class TestBooksTwCrawler(unittest.TestCase):
    def setUp(self):
        # self.app = create_app('testing')
        # self.app_context = self.app.app_context()
        # self.app_context.push()
        # db.create_all()
        # Role.insert_roles()
        # self.client = self.app.test_client(use_cookies=True)
        self.spider = BooksTwCrawler()

    def tearDown(self):
        # db.session.remove()
        # db.drop_all()
        # self.app_context.pop()
        self.spider = None

    # def test_home_page(self):
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('Stranger' in response.get_data(as_text=True))

    def test_search_from_isbn(self):
        self.spider.search_isbn('9789578423886')
        result_id = set()
        result_id.update(['0010823875','E050048572'])
        self.assertEqual(self.spider.prod_ids, result_id)

    @unittest.skip("test get_product")
    def test_get_product(self):
        ids = ["0010834816", "CN11708291", "F014313133"]
        name = ["Python 技術者們", "盜墓筆記十年", "A Scandal in Japan"]
        for id in ids:
            self.spider.get_product(ids)

        self.assertEqual(self.spider.prod_ids, result_id)





if __name__ == '__main__':
    unittest.main()
