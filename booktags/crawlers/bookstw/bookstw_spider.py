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
import sys
import re

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from datetime import datetime


from booktags.crawlers.base import BaseCrawler
# from booktags.flaskapp import db
# from booktags.db.basemodels import Book

# --------------------------------------------------------- common routines

class LoginRequireError(RequestException):
    """Login require"""





class BooksTwCrawler(BaseCrawler):
    """Crawler for bookstw

    """
    base_domain = "https://www.books.com.tw"
    search_domain = "https://search.books.com.tw"
    search_path = "/search/query/key/"
    protocol = "https:"

    def __init__(self):
        self.prod_ids=set()
        self.prods=set()
        self.cur_soup_block={}


    def search_isbn(self,isbn: str):
        """
        中文書 \d+
        簡體書 CN\d+
        外文書 F\d+
        電子書 E\d+
        :param: isbn
        :return: list
        """
        temp_ids = set()
        target_url = f"{self.search_domain}{self.search_path}{isbn}"
        search_soup = self.get_soup(target_url)
        result_block = search_soup.find('ul', "searchbook")
        for item in result_block.find_all('li', "item"):
            for a in item.find_all('a', {'rel': 'mid_name'}):
                # print(f"item url:{self.protocol}{a['href']}")
                id = re.findall(r"item[/](.*?)[/]", a['href'])
                # print(f"item id: {id}")
                temp_ids.update(id)
        # self.prod_ids.update(temp_ids)
        return temp_ids


    def get_soup(self, url: str) -> object:
        """

        :param url:
        :return: soup
        """
        # url = f"{self.base_domain}/products/{url}"


        try:
            res = requests.get(url)
            res.raise_for_status()

            if "請先登入會員" in res.text:
                raise LoginRequireError
                print("Login please")


        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except LoginRequireError as errl:
            print("Login required", errl)
            sys.exit(1)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        finally:
            pass

        soup = BeautifulSoup(res.text,"html.parser")

        # TODO : functional programming or?
        # self.cur_soup = soup
        return soup


    def get_blocks(self, soup: object) -> dict:
        """get_blocks

        head_block
        top_block
            title_block
            pub_block
            price_block
        bottom_block
            detail_block
            sort_block

        :param soup:
        :return:
        """
        # url = f"{self.base_domain}/products/{idx}"
        # soup=self.get_soup(url)

        head_block=soup.head
        top_block = \
        soup.select("div.container_24.main_wrap.clearfix > div > div.mod.type02_p01_wrap.clearfix > div.grid_10")[0]
        title_block = top_block.find('div', 'mod type02_p002 clearfix')
        pub_block = top_block.find('div', 'type02_p003 clearfix')
        price_block = top_block.find('ul', 'price')

        bottom_block = soup.select("div.grid_19.alpha > div.mod_b.type02_m058.clearfix > div")[0]
        detail_block = bottom_block.select('ul:nth-child(1)')[0]
        sort_block = bottom_block.find('ul', "sort")

        soup_block={
            # "id" : idx,
            "head_block" : head_block,
            # "top_block" : top_block,
            "title_block" : title_block,
            "pub_block" : pub_block,
            "price_block" : price_block,
            # "bottom_block" : bottom_block,
            "detail_block" : detail_block,
            "sort_block" : sort_block
        }

        # self.cur_soup_block=soup_block
        return soup_block


    def parse_head_block(self,head_block) -> dict:
        """
        name
        image
        url
        :return:
        """
        # head_block = self.cur_soup_block['head_block']

        metas = head_block.find_all('meta')
        cont = {meta.attrs['property']: meta.attrs['content'] for meta in metas if 'property' in meta.attrs}
        image = re.search(r'(https:\/\/www).*(jpg)', cont['og:image']).group(0)
        head_result = {
            "name" : cont["og:title"],
            "image" : image,
            "url" : cont["og:url"]
        }
        return head_result


    def parse_title_block(self,title_block) -> dict:
        """
        title

        if title_english
        if subtitle
        :return:
        """
        name = title_block.h1.text.strip()
        title_english = title_block.h2.text.strip()
        lst = name.split('：')
        title=lst[0]
        subtitle=name.lstrip(title+'：')

        title_result={
            "title" : title,
            "subtitle" : subtitle,
            "title_english" : title_english
        }

        return title_result


    def parse_pub_block(self,pub_block) -> dict:
        """
        author if many
        if author_origin
        if translator
        publisher
        date_published
        in_language

        :return:
        """
        # TODO: multiple author
        #  https://www.books.com.tw/products/0010794170

        pub_schema = {
            "作者": "author",
            "原文作者": "author_origin",
            "譯者": "translator",
            "出版社": "publisher",
            "出版日期": "date_published",
            "語言": "in_language"
        }

        cnt = len(pub_block.select('li'))

        b_in_language = pub_block.select('li')[cnt - 1].extract()
        b_date_published = pub_block.select('li')[cnt - 2].extract()
        b_publisher = pub_block.select('li')[cnt - 3].extract()
        b_author = pub_block.select('li')[0].extract()

        if "譯者" in pub_block.text:
            translator = pub_block.select('a')[-1].text.strip()
        else:
            translator = ""

        if "原文作者" in pub_block.text:
            author_origin = pub_block.select('a')[0].text.strip()
        else:
            author_origin = ""

        in_language=b_in_language.text.split('：')[1].strip()
        date_published_tmp = b_date_published.text.split('：')[1].strip()
        date_published = datetime.strptime(date_published_tmp, '%Y/%m/%d')

        publisher=b_publisher.select('span')[0].text.strip()

        author_tmp=b_author.contents[3].text.strip()
        author_list = author_tmp.split(',')
        author = author_list[0].strip()

        pub_result = {
            "author": author,
            "author_origin": author_origin,
            "publisher": publisher,
            "date_published": date_published,
            "in_language": in_language,
            "translator": translator
        }

        return pub_result




    def parse_price_block(self,price_block) -> dict:
        """
        price
        discount_rate
        discount_price

        if discount_date
        :return:
        """
        price_tmp = {}
        price_schema = {
            "定價": "price",
            "優惠期限": "discount_date",
            "優惠價": "discount_price"
        }

        for i in price_block.select('li'):
            if '：' not in i.text:
                continue
            field, value = i.text.split('：')
            for k, v in price_schema.items():
                if field == k:
                    price_tmp[v] = value

        price = price_tmp['price'].rstrip('元')
        discount_rate, discount_price = price_tmp['discount_price'].split('折')
        discount_price = discount_price.rstrip('元')

        if price_tmp['discount_date'] == None or price_tmp['discount_date'] == '':
            discount_date = None
        else:
            discount_date = datetime.strptime(price_tmp['discount_date'], '%Y年%m月%d日止')

        # discount_date_str = datetime.strftime(discount_date,"%Y/%m/%d")


        price_result = {
            "price": int(price),
            "discount_price": int(discount_price),
            "discount_rate": float(discount_price)/float(price),
            "discount_date": discount_date
        }

        return price_result


    def parse_detail_block(self,detail_block) -> dict:
        """
        isbn
        if series
        location_created
        parse specification

        :return:
        """
        # 規格：平裝 / 8.6 x 7.6 x 4.6 cm / 普通級
        # 規格：平裝 / 296頁 / 14.8 x 21 x 1.48 cm / 普通級 / 單色印刷 / 初版
        # 規格：平裝 / 1034頁 / 19 x 26 x 5.8 cm / 普通級 / 全彩印刷 / 九版
        # 規格：平裝 / 256頁 / 17 x 23 x 1.28 cm / 普通級 / 雙色印刷 / 初版
        if "叢書系列" in detail_block.text:
            isbn = detail_block.select('li')[0].text.split('：')[1].strip()
            series = detail_block.select('li')[1].text.split('：')[1].strip()
            specification = detail_block.select('li')[2].text.strip()
            location_created = detail_block.select('li')[3].text.split('：')[1].strip()
        else:
            isbn = detail_block.select('li')[0].text.split('：')[1].strip()
            series = ''
            specification = detail_block.select('li')[1].text.strip()
            location_created = detail_block.select('li')[2].text.split('：')[1].strip()

        spe_result = self.parse_specification(specification)
        number_pages= int(spe_result['number_pages'].rstrip(' 頁'))

        detial_result={
            "isbn": isbn,
            "series": series,
            "location_created": location_created,
            # specification
            "book_format": spe_result["book_format"],
            "number_pages": number_pages,
            "dimensions": spe_result["dimensions"],
            "content_rating": spe_result["content_rating"],
            "printing_color": spe_result["printing_color"],
            "book_edition": spe_result["book_edition"],
            "width": float(spe_result["width"]),
            "height": float(spe_result["height"]),
            "depth": float(spe_result["depth"])
        }
        return detial_result


    def parse_specification(self,spe: str) -> dict:
        """Parse specification

        specification
            book_format
            number_pages
            width
            height
            depth
            content_rating
            printing_color
            book_edition

        :param spe:
        :return:
        """
        spe = spe.lstrip("規格：")
        spe_tmp = [ele.strip() for ele in spe.split('/')]
        # TODO : paper_size : 25k, 16k ?
        schema = {"裝": "book_format",
                  "頁": "number_pages",
                  "cm": "dimensions",
                  "級": "content_rating",
                  "印刷": "printing_color",
                  "版": "book_edition"
                  }
        spe_result = {}
        for d in spe_tmp:
            for k, v in schema.items():
                if k in d:
                    spe_result[v] = d
        dia = spe_result['dimensions'].rstrip(' cm').split(' x ')
        spe_result['width'], spe_result['height'], spe_result['depth'] = dia

        return spe_result


    def parse_sort_block(self,sort_block) -> dict:
        """
        category
        :return:
        """
        # TODO: category
        # https://stackoverflow.com/questions/4896104/creating-a-tree-from-self-referential-tables-in-sqlalchemy
        category = ""
        for i in sort_block.find_all('li'):
            # print(i.text.split('：')[1])
            ele = i.text.split('：')[1]
            if len(sort_block.find_all('li')) >= 2:
                category = f"{category}|{ele}"
            else:
                category=ele
        category_result = {
            "category":category
        }
        return category_result


    def get_contents(self,soup: object) -> dict:
        """
        if summary
        if about_author
        if toc
        if preface

        :return:
        """
        # url = f"{self.base_domain}/products/{idx}"
        # soup = self.get_soup(url)

        schema={
            "內容簡介" : "summary",
            "作者介紹": "about_author",
            "目錄": "toc",
            "序": "preface"
        }

        contents_result={}
        for block in soup.find_all('div', 'mod_b type02_m057 clearfix'):
            block_title=block.h3.text.strip()
            block_content=block.find('div','content').text.strip()
            for key,value in schema.items():
                if block_title == key:
                    contents_result[value]=block_content
        return contents_result


    def get_book(self,idx: str) -> dict:
        """

        :return:
        """
        url = f"{self.base_domain}/products/{idx}"
        soup= self.get_soup(url)
        block=self.get_blocks(soup)

        head_result=self.parse_head_block(block['head_block'])
        title_result = self.parse_title_block(block['title_block'])
        pub_result = self.parse_pub_block(block['pub_block'])
        price_result = self.parse_price_block(block['price_block'])
        detail_result = self.parse_detail_block(block['detail_block'])
        sort_result = self.parse_sort_block(block['sort_block'])
        contents_result = self.get_contents(soup)

        book_dic={}
        book_dic.update(head_result)
        book_dic.update(title_result)
        book_dic.update(pub_result)
        book_dic.update(price_result)
        book_dic.update(detail_result)
        book_dic.update(sort_result)
        book_dic.update(contents_result)

        return book_dic


if __name__ == '__main__':
    pass