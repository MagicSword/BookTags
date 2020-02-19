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
import requests
from bs4 import BeautifulSoup

# --------------------------------------------------------- common routines

class Book():
    """Book class"""
    def __init__(self,id):
        self.id = str(id)
        self.isbn = ''
        self.title = ''
        self.subtitle = ''
        self.name_ori = ''
        self.author = ''
        self.author_other = ''
        self.publication_date = ''
        self.publisher = ''
        self.price = ''
        self.price_current = ''
        self.format = '' #paperback/softcover/hardcover
        self.pages = ''
        self.language = ''
        self.category = ''
        self.dimensions = ''  # 大小
        self.distribution_Area = ''
        self.summary = ''
        self.author_about = ''
        self.toc = ''
        self.description = ''
        self.imageurl = ''
        self.hackmd_meta = ''


    def fetchData(self):
        url = 'https://www.books.com.tw/products/' + self.id
        # add headers 20200217
        headers = {'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Referer': url,
                   'Connection': 'keep-alive'
                   }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.title = soup.find("meta", property="og:title")["content"]
        self.url = soup.find("meta", property="og:url")["content"]
        image = soup.find("meta", property="og:image")["content"]
        self.imageurl = re.search(r'(https:\/\/www).*.*(jpg)', image).group(0)
        desc = soup.find("meta", property="og:description")["content"]
        description = ''
        for li in desc.split('，'):
            new_li = ''.join(('* ', li, '\n'))
            description = description + new_li
        self.description = description

        self.hackmd_meta += '![' + self.title + '](' + self.imageurl + ' =50%x50%)' + '\n'
        self.hackmd_meta += '* [圖書資料](' + self.url + ')' + '\n'
        self.hackmd_meta += self.description


def get_hackmdmeta(bookid):
    book = Book(bookid)
    book.fetchData()
    return book.hackmd_meta

if __name__ == '__main__':
    pass