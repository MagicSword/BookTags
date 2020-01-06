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

from booktags.crawlers.base import BaseCrawler


# --------------------------------------------------------- common routines

class MetaNclCrawler(BaseCrawler):
    """

    meta_ncl	    臺灣書目整合查詢系統	http://metadata.ncl.edu.tw
    """
    base_domain = "http://metadata.ncl.edu.tw"
    search_domain = "http://metadata.ncl.edu.tw"
    search_path_isbn = "/search*cht/?searchtype=i&searcharg="
    protocol = "https:"

    def __init__(self):
        pass

    def search_isbn(self, isbn: str) -> list:
        """

        :return:
        """

        # urlsplit
        # <scheme>://<netloc>/<path>?<query>#<fragment>

        # urlparse
        # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
        search_url = f"{self.base_domain}{self.search_path_isbn}{isbn}"
        soup = self.get_soup(search_url)

        head_block = soup.find_all("td", "browseHeaderData")[0]
        result_count = int(head_block.text.strip().split('之')[1].strip().rstrip(')'))

        # 換頁
        # /search~S10*cht/tpython/tpython/55,873,2091,E/2browse
        # 873 總數，55 想跳的筆數

        result_list = soup.find_all('tr', 'briefCitRow')

        result_urls = []
        # TODO : 如果結果超過一頁
        for item in result_list:
            url = item.select('.briefcitTitle a')[0]['href']
            # print(f"url:{url}")
            result_urls.append(url)
        # print(f"result_urls:{result_urls}")
        return result_urls

    def get_blocks(self, soup: object) -> dict:
        """

        :param soup:
        :return:
        """
        top_block = soup.find_all('div', 'bibContent')[0]
        mid_block = soup.find_all('table', 'bibItems')[0]
        bot_block = soup.find_all('div', 'bibContent')[1]

        soup_block = {
            # "id" : idx,
            "top_block": top_block,
            "mid_block": mid_block,
            "bot_block": bot_block
        }

        return soup_block


if __name__ == '__main__':
    pass