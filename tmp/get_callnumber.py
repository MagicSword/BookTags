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


import os
from os import listdir
import click
from marcx import FatRecord
import requests
import re
from bs4 import BeautifulSoup
import json
import tqdm
import re
from os.path import isfile, isdir, join

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    filename='get_callnumber_log.txt')

# --------------------------------------------------------- common routines

class Boos():
    def __init__(self, id,isbn,callnumber, fail):
        self.id = id
        self.isbn = isbn
        self.callnumber = callnumber
        self.fail = fail



def get_all_filenames():
    # 指定要列出所有檔案的目錄
    mypath = "./marc/"

    # 取得所有檔案與子目錄名稱
    files = listdir(mypath)

    # 以迴圈處理
    # for f in files:
    #     #   # 產生檔案的絕對路徑
    #     #   fullpath = join(mypath, f)
    #     #   # 判斷 fullpath 是檔案還是目錄
    #     #   if isfile(fullpath):
    #     #     print("檔案：", f)
    #     #   elif isdir(fullpath):
    #     #     print("目錄：", f)
    return files


def get_callnmuber_nbin(isbn):
    """get callnumber form nbin net

    :return:
    """
    # isbn = "9789863125501"
    # url = "http://nbinet3.ncl.edu.tw/search*cht/?searchtype=i&searcharg=9789863125501"
    domain = "http://nbinet3.ncl.edu.tw"
    base_url = "http://nbinet3.ncl.edu.tw/search*cht/?searchtype=i&searcharg="
    # Search List
    #isbn = k['isbn']
    callnum = ""
    try:
        url = base_url + isbn
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        url_single_book = soup.find_all("span", {"class": "briefcitTitle"})
        ts = url_single_book[1].a

        # Single book page
        url_one = domain + ts['href']
        # print(url_one)
        res_one = requests.get(url_one)
        soup_one = BeautifulSoup(res_one.text, "html.parser")
        field = soup_one.find_all("tr", {"class": "bibItemsEntry"})
        callnum = field[0].a.text
    except:
        pass
    else:
        pass
    return callnum

def get_callnumber_marc(book):
    """get callnumber form marc file

    :return:
    """
    filename = "%s%s-%s.%s" % ('./marc/',book['id'] ,book['isbn'],'marc')
    logging.info("Open file from : {}".format(filename))
    with open(filename,'rb') as fd:
        try:
            record = FatRecord(fd.read())
        except:
            pass
        else:
            tmp_list = list(record.itervalues('200.a','805.d','805.e','805.y'))
            book.update(author = tmp_list[0])
            for i in range(1,3):
                tmp_callnum = ' '.join(tmp_list[i])
            book.update(callnumber = tmp_callnum)

    return tmp_callnum

@click.command()
@click.option('-s', '--isbn', help='Library book ISBN')
def cli(isbn):
    """

    :return:
    """
    # 讀 所有 目錄下的檔名
    # callnumber = get_callnumber_marc()
    row_fail = []
    filenames = get_all_filenames()

    for val in filenames:
        if val.endswith('.fail'):
            fail = "fail"
        else:
            fail = ""

        fields = val.split('.')
        id = fields[0].split('-')[0]
        isbn = fields[0].split('-')[1]
        callnum = "978"
        #print("Fail : {} - {}".format(id, isbn))
        row_fail.append({"id":id,"isbn": isbn,"callnumber":callnum,"fail":fail})



    for k in row_fail:
        # if k['fail'] == 'fail':
        #     #print(k['isbn'] + ".fail")
        #     k['callnumber'] = get_callnmuber_nbin(k)
        # else:
        #     #print(k['isbn'] + '.success')
        #     #k['callnumber'] = get_callnumber_marc(k)
        k['callnumber'] = get_callnmuber_nbin(k['isbn'])




    for i in row_fail:
        #i.update({"callnumber":"999"})
        msg = "{} - {} - {} : {}".format(i['id'], i['isbn'],i["fail"],i["callnumber"])
        print(msg)
        logging.info(msg)
        #filename = "%s%s-%s.%s" % ('./marc/', i['id'], i['isbn'], 'marc')

    file_save = './bookshelf_callnumber.txt'
    with open(file_save,'w',encoding="UTF-8") as fd:
        print("Save to book: %s" % file_save)
        json.dump(row_fail,fd)




if __name__ == '__main__':
    cli()