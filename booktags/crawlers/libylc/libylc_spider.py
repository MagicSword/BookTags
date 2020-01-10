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

from typing import List,Dict
from abc  import ABC

import re
import os
import requests
from bs4 import BeautifulSoup

from booktags import ASSETS_DIR
from booktags.crawlers.base import BaseCrawler


# --------------------------------------------------------- common routines


class LibYlcCrawler(BaseCrawler):
    """
    Search 雲林縣公共圖書館	    http://library.ylccb.gov.tw/webpacIndex.jsp
    1. regular data
    2. marc


    """
    base_domain="http://library.ylccb.gov.tw"
    search_domain="http://library.ylccb.gov.tw"
    # 這是簡單的 booksearch.do , 長列表是 bookSearchList.do
    search_path="/booksearch.do?searchtype=simplesearch&execodeHidden=true&execode=webpac.dataType.book&authoriz=1&search_field=ISBN&search_input="
    exportiso_path="/exportISOPage.jsp?books="

    book_path="/bookDetail.do?id="
    book_top_path="/maintain/bookDetailAssdataAjax.do?id="
    book_bot_path="/maintain/HoldListForBookDetailAjax.do?id="

    marc_path=os.path.join(ASSETS_DIR,"libylc_marc")

    class LibYlcBook(ABC):
        """Base class to handle single book

        """

        def __init__(self,id):
            self.id=id  #library id
            self.marc="" #binary marc

        





    def __init__(self):
        pass


    def search_isbn(self,isbn: str) -> List[str]:
        """

        :param isbn:
        :return:
        """

        url = f"{self.search_domain}{self.search_path}{isbn}"
        ref_url= url

        headers = {'DNT': '1',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Referer': ref_url,
                   'Cookie': 'cookieActived=true; JSESSIONID=92BA9371A15172528F3815B2998B879C; webpacslb-HTTP-80=PDLLFDMA; __utmt=1; __utma=240264336.628942217.1430060220.1430060220.1430060220.1; __utmb=240264336.2.10.1430060220; __utmc=240264336; __utmz=240264336.1430060220.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
                   'Connection': 'keep-alive'
                   }

        # TODO : 如果結果有多頁？
        # 找 class = "keysearch"
        response_search = requests.get(url, headers=headers)
        # soup = BeautifulSoup(response_search.text, 'html.parser')
        # num_result = soup.find_all(id="totalpage")[0].text
        # print("Get {} results.".format(num_result))
        try:
            # isbn 9789864768813
            # <script>parent.location.href = 'bookDetail.do?id=564336';</script>
            # get_libraryid()
            libraryid = []
            libraryid_result = re.findall('bookDetail.do\?id=(\d+)', response_search.text)
            [libraryid.append(i) for i in libraryid_result if not i in libraryid]

        except:
            print("Exception occurred in search_isbn")
        else:
            return libraryid

    def get_soup(self, url: str,ref_url:str) -> object:
        """Get a BeautifulSoup object.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response

        :param url:
        :return: :class: `bs4.BeautifulSoup` object
        :rtype: bs4.BeautifulSoup
        """
        # url = f"{self.base_domain}/products/{url}"





        headers = {'DNT': '1',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Referer': ref_url,
                   'Cookie': 'cookieActived=true; JSESSIONID=92BA9371A15172528F3815B2998B879C; webpacslb-HTTP-80=PDLLFDMA; __utmt=1; __utma=240264336.628942217.1430060220.1430060220.1430060220.1; __utmb=240264336.2.10.1430060220; __utmc=240264336; __utmz=240264336.1430060220.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
                   'Connection': 'keep-alive'
                   }


        try:
            res = requests.get(url,headers=headers)
            res.raise_for_status()

            # if "請先登入會員" in res.text:
            #     raise LoginRequireError
            #     print("Login please")

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        # except LoginRequireError as errl:
        #     print("Login required", errl)
        #     sys.exit(1)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        finally:
            pass

        soup = BeautifulSoup(res.text,"html.parser")

        # Fixed : functional programming or?
        # class method use self.var  ,
        # standalone func return var
        # self.cur_soup = soup
        return soup


    def fetch_blocks(self, idx: str) -> Dict[str,object]:
        """

        :rtype: Dict[str,object]
        :return: Dict[str,object]
        """
        """
        image -> id="myImagesSlideBox" class="myImagesSlideBox" -> <img title=圖書
        書目 -> <td.mainconC
        
        其他
        <div.allDetail
        館藏,
            <table class='order'
        簡介,作者簡介,標籤,收藏,評論,評分,引用     

        """
        # page
        # http://library.ylccb.gov.tw/bookDetail.do?id=580659
        # top_block
        # http://library.ylccb.gov.tw/maintain/bookDetailAssdataAjax.do?id=580659
        # detail
        # http://library.ylccb.gov.tw/maintain/HoldListForBookDetailAjax.do?id=580659

        book_url=f"{self.base_domain}{self.book_path}{idx}"
        ref_url=f"{self.base_domain}{self.search_path}{idx}"
        soup=self.get_soup(book_url,ref_url)

        cover_block=soup.select('#myImagesSlideBox')[0]
        top_block=self.get_soup(f"{self.base_domain}{self.book_top_path}{idx}",ref_url)
        bot_block=self.get_soup(f"{self.base_domain}{self.book_bot_path}{idx}",ref_url)

        soup_block={
            "cover_block":cover_block,
            "top_block":top_block,
            "bot_block":bot_block
        }
        return soup_block

    def fetch_marc(self, idx: str) -> object:
        """

        :param idx:
        :return:
        """
        book_url=f"{self.base_domain}{self.exportiso_path}{idx}"
        try:
            res=requests.get(book_url)
            res.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        finally:
            pass

        marc_res = res

        return marc_res

    def save_marc(self,idx: str,isbn: str):
        """

        :param filepath:
        :return:
        """
        import os
        # base_url = "http://library.ylccb.gov.tw/exportISOPage.jsp?books="
        book_url=f"{self.base_domain}{self.exportiso_path}{idx}"
        marc_res=self.fetch_marc(idx)
        filename = f"{isbn}-{idx}{'.marc'}"
        full_path=os.path.join(self.marc_path,filename)

        # marc 編碼 utf-8
        try:
            if not os.path.exists(self.marc_path):
                os.makedirs(self.marc_path)
            with open(full_path,"wb") as fd:
                print(f"Saving to : {full_path}")
                fd.write(marc_res.content)
        except IOError as erri:
            print("IOError:", erri)
        finally:
            pass

    def marc_tojson(self):
        """

        :return:
        """
        pass


    def parse_marc(self,idx: str) -> Dict[str,str]:
        """

        :param marc_res:
        :return:
        """
        pass


    def parse_cover_block(self,cover_block: object) -> Dict[str,str]:
        """

        :param cover_block:
        :return:
        """
        image=cover_block.find_all('img')[3]['src'].strip()

        cover_result={
            "image":image
        }

        return cover_result


    def parse_top_block(self,top_block: object) -> Dict[str,str]:
        """

        :param top_block:
        :return:
        """
        top_schema={
             "題名": "name",
             "作者": "author",
             "語文": "in_language",
             "ISBN/ISSN/ISRC": "isbn",
             "版本": "book_edition",
             "出版社": "publisher",
             "出版地": "location_created",
             "簡介": "summary"
                }

        result = {}

        for table in top_block.select('table'):
            k, v = table.select('td')
            result[k.text.strip('：')] = v.text.strip()

        top_result={}
        for label,td in result.items():
            for k,v in top_schema.items():
                if label==k:
                    top_result[v]=td

        # isbn remove "-"
        if '-' in top_result['isbn']:
            isbn=top_result['isbn'].replace("-","")
            top_result['isbn']=isbn

        return top_result


    def parse_bot_block(self,bot_block: object) -> Dict[str,str]:
        """
        館藏,
            <table class='order'
            簡介,作者簡介,標籤,收藏,評論,評分,引用
            ignore other tabs

            login, dynamic ajax

        :param bot_block:
        :return:
        """
        bot_schema = {
                "#" : "sn",
                "條碼號" : "barcode",
                "館藏地 / 室" : "keepsite",
                "索書號" : "callnum",
                "資料類型" : "media_type",
                "目前狀態 / 到期日" : "due_date",
                "附件" : "attachment",
                "預約" : "reservation"
        }

        table = bot_block.select('table.order')[0]
        th_row=table.tr.extract()
        headers = [header.text.strip() for header in th_row.select("tr th")]
        results = [{headers[i]: cell.text.strip() for i, cell in enumerate(row.select("td"))} for row in table.select("tr")]


        # http://library.ylccb.gov.tw/bookDetail.do?id=10641
        # TODO: 館藏:多筆資料，統計 ，目前跳過
        bot_result={
            "number_copies" : 5,
            "barcode": "00640000219629",
            "keepsite": "文化處圖書室/文化處開架式閱覽室",
            "callnum": "610 4423 2018",
            "media_type": "一般圖書/一般",
            "due_date": "已被外借 / 2020-01-17",
            "attachment": "1張光碟片(MP3)+ 1本手冊",
            "reservation": " / 0人預約"
        }

        return bot_result


    def get_book(self,idx: str) -> Dict[str,str]:
        """

        :param idx:
        :return:
        """
        pass


if __name__ == '__main__':
    pass
