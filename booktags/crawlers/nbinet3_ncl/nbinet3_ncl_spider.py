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

class Nbinet3NlcCrawler(BaseCrawler):
    """

    nbinet3_ncl	    NBINet圖書聯合目錄	    http://nbinet3.ncl.edu.tw/screens/opacmenu_cht.html
    """
    base_domain = "http://nbinet3.ncl.edu.tw"
    search_domain = "http://nbinet3.ncl.edu.tw"
    search_path_isbn = "/search*cht/?searchtype=i&searcharg="

    protocol = "https:"




    def __init__(self):
        pass

    def search_isbn(self,isbn: str) -> list:
        """

        :return:
        """

        # urlsplit
        # <scheme>://<netloc>/<path>?<query>#<fragment>

        # urlparse
        # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
        search_url = f"{self.base_domain}{self.search_path_isbn}{isbn}"
        soup = self.get_soup(search_url)

        head_block = soup.find_all("td","browseHeaderData")[0]
        result_count=int(head_block.text.strip().split('之')[1].strip().rstrip(')'))

        # 換頁
        # /search~S10*cht/tpython/tpython/55,873,2091,E/2browse
        # 873 總數，55 想跳的筆數

        result_list=soup.find_all('tr','briefCitRow')

        result_urls = []
        # TODO : 如果結果超過一頁
        for item in result_list:
            url=item.select('.briefcitTitle a')[0]['href']
            # print(f"url:{url}")
            result_urls.append(url)
        # print(f"result_urls:{result_urls}")
        return result_urls

    def get_blocks(self,soup: object) -> dict:
        """

        :param soup:
        :return:
        """
        top_block=soup.find_all('div','bibContent')[0]
        mid_block=soup.find_all('table','bibItems')[0]
        bot_block=soup.find_all('div','bibContent')[1]


        soup_block={
            # "id" : idx,
            "top_block" : top_block,
            "mid_block" : mid_block,
            "bot_block" : bot_block
        }

        return soup_block

    def parse_top_block(self,top_block: object) -> dict:
        """

        :param bibContent_top:
        :return:
        """


        return top_result

    def parse_mid_block(self,mid_block: object) -> list:
        """

        :return:
        """
        mid_tmp = []
        for item in mid_block.find_all('tr', 'bibItemsEntry'):
            # print(item.select('tr > td:nth-child(2)')[0].text)
            callnum = item.select('tr > td:nth-child(2)')[0].text.strip()
            mid_tmp.append(callnum)

        mid_result = {}

        return mid_tmp

    def parse_bot_block(self,bot_block: object) -> dict:
        """

        :param bot_block:
        :return:
        """


        return bot_result

    def get_book(self,isbn: str) -> dict:
        """

        :return:
        """
        # < div.bibMain
        #  < div.bibInfo
        #   < div.bibContent(上半部
        #       < table.bibDetail
        #        < tr.bibInfoEntry
        #        < td.bibInfoLabel
        #        < td.bibInfoData
        #   < table.bibItems
        #     < tr.bibItemsHeader
        #     < tr.bibItemsEntry
        #      < td
        #        < a

        return book_dic





if __name__ == '__main__':
    pass