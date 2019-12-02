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

from marcx import FatRecord
import requests
import click
import json
import re
from bs4 import BeautifulSoup
# --------------------------------------------------------- common routines

DOMAIN = "http://library.ylccb.gov.tw"

#URL = "http://library.ylccb.gov.tw/exportISOPage.jsp?books=573643"
#libraryid = "573643"



def libraryid_to_marc(libraryid):
    """Libarary Id  to marc format"""
    base_url = "http://library.ylccb.gov.tw/exportISOPage.jsp?books="
    url = base_url + libraryid
    res = requests.get(url)
    record = FatRecord(data=res.content)
    #print(filename)
    return(record)


def save_marc_record(record,format):
    """Save marc to json or marc file
    default filename :  library.format(json, or marc)
    """
    for val in record.itervalues('001'):
        libraryid = val
    filename = libraryid + '.' + format
    # TODO: save file codec : utf8 , latin-1
    # open(filename,'w',encoding='UTF-8')
    print("Saving file to : {}".format(filename))
    if format == 'json':
        with open(filename,'w') as fd:
            json.dump(record.as_json(),fd)
    else:
        with open(filename,'wb') as fd:
            fd.write(record.as_marc())



def isbn_to_libraryid(isbn):
    """ISBN to library Id

    """
    #validate  isbn
    # base_search_url = "http://library.ylccb.gov.tw/bookSearchList.do"
    # input_obj = {'searchtype':'simplesearch','search_field': 'ISBN','search_input': isbn}
    # res = requests.get(base_search_url,params=input_obj,allow_redirects=True)
    # action = bookSearchList.do , method = GET
    # execode
    #
    # http://library.ylccb.gov.tw/bookSearchList.do?searchtype=simplesearch&execodeHidden=true&execode=&search_field=FullText&search_input=mongodb&searchsymbol=hyLibCore.webpac.search.common_symbol&keepsitelimit=#searchtype=simplesearch&execodeHidden=true&execode=&search_field=FullText&search_input=mongodb&searchsymbol=hyLibCore.webpac.search.common_symbol&keepsitelimit=&resid=189071364&nowpage=1
    #
    # http://library.ylccb.gov.tw/bookSearchList.do?search_field=ISBN&search_input=9789864768240
    # http://library.ylccb.gov.tw/bookDetail.do?id=573643
    # fail  search to result
    # TODO: ISBN 可能會 1. 缺失 (沒書，或沒 isbn)  2. 有多個記錄(同 isbn 多館藏位置)

    headers = {'DNT':'1',
           'Accept-Encoding':'gzip, deflate, sdch',
           'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
           'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Referer':'http://library.ylccb.gov.tw/bookSearchList.do?searchtype=simplesearch&execodeHidden=true&execode=webpac.dataType.book&authoriz=1&search_field=ISBN&search_input=' + isbn,
           'Cookie':'cookieActived=true; JSESSIONID=92BA9371A15172528F3815B2998B879C; webpacslb-HTTP-80=PDLLFDMA; __utmt=1; __utma=240264336.628942217.1430060220.1430060220.1430060220.1; __utmb=240264336.2.10.1430060220; __utmc=240264336; __utmz=240264336.1430060220.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
           'Connection':'keep-alive'
           }

    url1 = 'http://library.ylccb.gov.tw/booksearch.do?searchtype=simplesearch&execodeHidden=true&execode=webpac.dataType.book&authoriz=1&search_field=ISBN&search_input=' + isbn
    q1 = requests.get(url1,headers=headers)
    libraryid = re.findall('bookDetail.do\?id=(\d+)' ,q1.text)

    print(libraryid[0])
    return libraryid[0]


def get_metadata(libraryid):
    """from library page get
    book title, image_url, description
    """
    base_url = "http://library.ylccb.gov.tw/bookDetail.do?id="
    url = base_url + libraryid
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find("meta", property="og:title")["content"]
    # self.url = soup.find("meta", property="og:url")["content"]
    image_url = soup.find('meta', property='og:image')['content']
    desc_tag = soup.select('meta[name="description"]')
    description = desc_tag[0].attrs['content']

    #self.imageurl = re.search(r'(https:\/\/www).*.*(jpg)', image).group(0)
    # desc = soup.find("meta", name="description")["content"]
    #     # description = ''
    #     # for li in desc.split('，'):
    #     #     new_li = ''.join(('* ', li, '\n'))
    #     #     description = description + new_li
    #     #     self.description = description
    return (title,image_url,description)




def get_keepsite():
    """
    Get info of where the book store
    http://library.ylccb.gov.tw/bookDetail.do?id=573643
    <!--  標籤內容 Start  -->
    <div class="allDetail">
    動態表格, 隱藏內容

    館藏 keepsite
    簡介 indexBook
    作者簡介 indexAuthor
    標籤 tag
    收藏 collection
    評論 discuss
    評分 point
    引用 trackback

    <table class="order">
    <!--  標籤內容 End  -->
    :return:
    """
    pass

def print_marc_record(record):
    """Print MARC record

    :param record:
    :return: console print
    """
    recnum = 0
    for tield_contents in record.get_fields():
        recnum += 1
        print('%09d' % recnum, ' ', tield_contents.tag, '  ', ' L', tield_contents.value())


@click.command()
@click.option('-id', '--libraryid', help='Library book id', default='')
@click.option('-f', '--format', help='output format : json or marc')
def cli(libraryid,format):
    """Query library book and  Save to file.format(json or marc)"""
    current_record = libraryid_to_marc(libraryid)
    if format:
        save_marc_record(current_record,format)
    else:
        print_marc_record(current_record)

if __name__ == '__main__':
    cli()
