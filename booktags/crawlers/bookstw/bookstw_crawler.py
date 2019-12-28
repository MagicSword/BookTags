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

import os
import re
import datetime
import pandas
import requests
from bs4 import BeautifulSoup


from ..base import BaseCrawler
from ..base import baseschema
"""
https://search.books.com.tw/search/query/key/9789578423886/

圖書/中文書
https://search.books.com.tw/search/query/cat/1/qsub/001/key/9789578423886/

精準 search
https://search.books.com.tw/search/query/fm/0/bfm/1/key/%E5%BF%AB%E6%A8%82%E7%8E%8B%E5%AD%90%20%E4%B8%8D%E5%BF%AB
模糊 search
https://search.books.com.tw/search/query/fm/1/bfm/2/key/%E5%BF%AB%E6%A8%82%E7%8E%8B%E5%AD%90%20%E4%B8%8D%E5%BF%AB

single book url
https://www.books.com.tw/products/0010823875

"""
bookstw_schema = baseschema
bookstw_schema.update(dict(discount_price={"type": "int", "required": False, "nullable": True},
                           discount_rate={"type": "float", "required": False, "nullable": True},
                           discount_date={"type": "date", "required": False, "nullable": True},
                           pub_date={"type": "date", "required": False, "nullable": True}))

# bookstw pub_date
# def to_date(s):
#     return datetime.strptime(s, '%Y/%m/%d')




class BooksTwCrawler(BaseCrawler):
    """
    Search books.com.tw book
    """
    base_domain = "https://www.books.com.tw"
    search_domain = "https://search.books.com.tw"
    search_path = "/search/query/key/"
    protocol = "https:"

    def __init__(self) -> object:
        self.bookstw_result_id = []

    def search_isbn(self, isbn: str) -> list:
        """
        https://search.books.com.tw/search/query/key/9789578423886
        :param: isbn
        :return: bookstw_id list
        """
        #empty result list
        self.bookstw_result_id = []
        target_url = f"{self.search_domain}{self.search_path}{isbn}"
        search_res = requests.get(target_url)
        search_soup = BeautifulSoup(search_res.text,"html.parser")
        result_block = search_soup.find('ul', "searchbook")
        for item in result_block.find_all('li', "item"):
            for a in item.find_all('a', {'rel': 'mid_name'}):
                print(f"item url:{self.protocol}{a['href']}")
                id = re.findall(r"item/([a-zA-Z0-9]\d+)", a['href'])
                print(f"item id: {a['href']}")
                self.bookstw_result_id.append(id[0])


    def search_keyword(self, title: str) -> list:
        """
        :param: keyword
        :return: bookstw_id
        程式設計師從零開始邁向架構師之路
        https://search.books.com.tw/search/query/key/%E7%A8%8B%E5%BC%8F%E8%A8%AD%E8%A8%88%E5%B8%AB%E5%BE%9E%E9%9B%B6%E9%96%8B%E5%A7%8B%E9%82%81%E5%90%91%E6%9E%B6%E6%A7%8B%E5%B8%AB%E4%B9%8B%E8%B7%AF
        ['0010842548']
        """
        pass

    def search_author(self, author: str) -> list:
        """
        :param: author
        :return: bookstw_id
        François Chollet
        https://search.books.com.tw/search/query/cat/all/key/Fran%C3%A7ois+Chollet/adv_author/1
        0010822932
        https://search.books.com.tw/redirect/move/key/Fran%C3%A7ois+Chollet/area/mid/item/0010822932/page/1/idx/1/cat/001/pdf/1
        """
        pass

    def searchby_pubid(self,  pubid: str) -> list:
        """

        :param pubid:
        :return:
        旗標 ?pubid=flag
        https://www.books.com.tw/web/sys_puballb/books/?pubid=flag
        """
        pass

    def get_productlist(self, product_id: list) -> list:
        """

        :param product_id:
        :return: dict
        https://www.books.com.tw/products/0010823875
        """

        for idx,id in enumerate(product_id):
            url = f"{self.base_domain}/products/{id}"

    def get_product(self, id: str) -> dict:
        """

        :param id:
        :return: dict
        https://www.books.com.tw/products/0010823875

                # 中文書，簡體書，外文書
        中文書：title,(title_eng),author,publisher,pub_date,language
        簡體書：title,title_eng,author,translator,publisher,pub_date,language
        外文書：title,author,publisher,pub_date,language

        div.grid_10
            div["mod type02_p002 clearfix"]
                title
                subtitle
                tltle_origin - eng title
            div["type02_p003 clearfix"]
                author
                translator - if origin exist
                publisher
                pub_date
                language
            div["cnt_prod002 clearfix"]
                price
                discount
                discount_date
                discount_rate
        """
        url = f"{self.base_domain}/products/{id}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text,"html.parser")

        # TODO: pass meta['og:description']  , hard to parse

        ############## meta block
        image = soup.find("meta", property="og:image")["content"]
        url_image = re.search(r'(https:\/\/www).*.*(jpg)', image).group(0)
        url_product = soup.find("meta", property="og:url")["content"]

        ##############  parse block
        top_block = \
        soup.select("div.container_24.main_wrap.clearfix > div > div.mod.type02_p01_wrap.clearfix > div.grid_10")[0]
        t_title_block = top_block.find('div', 'mod type02_p002 clearfix')
        t_pub_block = top_block.find('div', 'type02_p003 clearfix')
        t_price_block = top_block.find('ul', 'price')

        bottom_block = soup.select("div.grid_19.alpha > div.mod_b.type02_m058.clearfix > div")[0]
        b_detail_block = bottom_block.select('ul:nth-child(1)')[0]
        b_sort_block = bottom_block.find('ul', "sort")

        ##############  top_block > t_title_block
        title, subtitle = t_title_block.h1.text.split('：')
        title_eng = t_title_block.h2.text

        # title_full = soup.find("meta", property="og:title")["content"]
        # self.parse_title(title_full)
        ##############  top_block > t_pub_block

        ##############  top_block > t_price_block

        ##############  bottom_block
        ##############  sammary block


        # title block

        # fill title , and subtitle if exist


        # div["type02_p003 clearfix"]
        pub_result = self.parse_t_pub_block(t_pub_block)
        author = pub_result['author']
        publisher = pub_result['publisher']
        pub_date = pub_result['pub_date']
        language = pub_result['language']
        # 如果是外文書，會有 譯者
        translator = pub_result['translator']

        # price block
        price = t_price_block.select('li:nth-child(1) > em')[0].text
        discount_rate = t_price_block.select('li:nth-child(2) > strong:nth-child(1)')[0].text
        discount_date = t_price_block.select('li:nth-child(3)')[0].text.split('：')[1]

        price_result = self.parse_t_price_block(t_price_block)
        price = price_result['price']
        discount_rate, discount_price = price_result['discount_price'].split('折')
        discount_price = discount_price.rstrip('元')
        discount_date = datetime.strptime(price_result['discount_date'], '%Y年%m月%d日止')



        # summary

        summary = soup.select("div.container_24.main_wrap.clearfix > div > div:nth-child(3) > div.grid_19.alpha > div:nth-child(1) > div")[0].text.strip()
        summary_author = soup.select("div.container_24.main_wrap.clearfix > div > div:nth-child(3) > div.grid_19.alpha > div:nth-child(2) > div")[0].text.strip()
        toc = soup.select('#M201105_0_getProdTextInfo_P00a400020009_h2')[0].text.strip()


        """
        ISBN：9789571380544
        叢書系列：People
        規格：平裝 / 296頁 / 14.8 x 21 x 1.48 cm / 普通級 / 單色印刷 / 初版
        出版地：台灣
        本書分類：人文史地> 台灣史地> 人物史/傳記
        本書分類：社會科學> 報導文學
        """

        # bottom info block
        bottom_block = soup.select("div.grid_19.alpha > div.mod_b.type02_m058.clearfix > div")[0]
        bottom_info = {}

        for ele in bottom_block.ul:
            field, value = ele.text.split('：')
            bottom_info[field] = value

        isbn = bottom_info['ISBN']
        pub_location = bottom_info['出版地']

        if "叢書系列" in bottom_block.text:
            serials = bottom_info["叢書系列"]

        # 規格：平裝 / 576頁 / 17 x 23 x 2.9 cm / 普通級 / 單色印刷 / 初版
        # binding / pages / dimensions / content_rating / print_color / edition
        specification = bottom_info["規格"]
        speci_list = self.parse_specification(specification)

        pages = speci_list['']
        binding = speci_list['']
        dimensions = speci_list['']

        

        # 本書分類：電腦資訊> 程式設計/APP開發> Python
        categories = self.parse_category(b_sort_block)



    def parse_title(self, title_full: str) -> list:
        """

        :type title_full: str
        :param title_full:
        :return: list
        """
        if '：' in title_full:
            self.title, self.subtitle = title_full.split('：')
        else:
            self.title = title_full

    def parse_t_pub_block(self, t_pub_block: object) -> dict:
        """

        :param t_pub_block: bs4.element.Tag
        :return: dict
        """
        author = t_pub_block.select("ul > li:nth-child(1) > a:nth-child(2)")[0].text
        pub_subblock = t_pub_block.select("div.type02_p003.clearfix > ul > li:nth-child(2)")[0]
        publisher = pub_subblock.find('span').text
        pub_location = pub_subblock.find_all('li')[1].text.split('：')[1].strip()
        language = pub_subblock.find_all('li')[2].text.split('：')[1].strip()

        if '譯者' in t_pub_block.text:
            translator = pub_subblock.find('a').text

        pub = {
            "author" : author,
            "publisher" : publisher,
            "pub_location" : pub_location,
            "language" : language,
            "translator" : translator
        }

        return pub

    def parse_t_price_block(self, t_price_block: object) -> dict:
        """

        :param t_price_block: bs4.element.Tag
        :return: dict
        """
        price_result = {}
        price_schema = {
            "定價": "price",
            "優惠價": "discount_price",
            "優惠期限": "discount_date"
        }

        for i in t_price_block.select('li'):
            field, value = i.text.split('：')
            for k, v in price_schema.items():
                if field == k:
                    price_result[v] = value

        return price_result

    def parse_specification(self, spe: str) -> dict:
        """

        :param spe:
        :return: dict
        規格：平裝 / 8.6 x 7.6 x 4.6 cm / 普通級
        規格：平裝 / 296頁 / 14.8 x 21 x 1.48 cm / 普通級 / 單色印刷 / 初版
        規格：平裝 / 1034頁 / 19 x 26 x 5.8 cm / 普通級 / 全彩印刷 / 九版
        規格：平裝 / 256頁 / 17 x 23 x 1.28 cm / 普通級 / 雙色印刷 / 初版
        """
        spe_tmp = [ele.strip() for ele in spe.split('/')]
        schema = {"裝": "binding",
                  "頁": "pages",
                  "cm": "dimensions",
                  "級": "content_rating",
                  "印刷": "print_color",
                  "版": "edition"
                  }
        spe_result = {}
        for d in spe_tmp:
            for k, v in schema.items():
                if k in d:
                    spe_result[v] = d

        return spe_result

    def parse_category(self, b_sort_block: object) -> list:
        """

        :param b_sort_block: bs4.Element.Tags
        :return: list
        """
        categories = []
        # sort_block = bottom_block.find('ul', "sort")
        for i in b_sort_block.find_all('li'):
            # print(i.text.split('：')[1])
            categories.append(i.text.split('：')[1])


    def get_events(self):
        df = pandas.read_csv(
            "https://raw.githubusercontent.com/python-organizers/conferences/master/2020.csv",
            quoting=1,
            encoding="utf-8",
            dtype=str,
        )
        df = df.fillna("")

        for event in df.to_dict(orient="records"):
            location = event["Location"].split(",")
            city = state = country = None
            if len(location) == 2:
                city = location[0].strip()
                country = location[1].strip()
            elif len(location) == 3:
                city = location[0].strip()
                state = location[1].strip()
                country = event["Country"]

            cfp_end_date = (
                event["Talk Deadline"] if event["Talk Deadline"] else "1970-01-01"
            )
            cfp_open = (
                True
                if datetime.datetime.now() < datetime.datetime.strptime(cfp_end_date, "%Y-%m-%d")
                else False
            )
            e = {
                "name": event["Subject"],
                "url": event["Website URL"],
                "city": city,
                "state": state,
                "country": country,
                "cfp_open": cfp_open,
                "cfp_end_date": cfp_end_date,
                "start_date": event["Start Date"],
                "end_date": event["End Date"],
                "source": "https://github.com/python-organizers/conferences",
                "tags": ["python"],
                "kind": "conference",
                "by": "bot",
            }
            self.events.append(e)


if __name__ == '__main__':
    pass