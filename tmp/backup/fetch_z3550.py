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
# https://hazy.today/1686-%E5%88%A9%E7%94%A8%20API%20%E5%92%8C%20Z39.50%20%E6%93%B7%E5%8F%96%E5%9C%96%E6%9B%B8%E9%A4%A8%E7%9A%84%E8%B3%87%E6%96%99/
#
# $ python fetch_z3550.py （z39.50 伺服器地址）（z39.50 伺服器端口）（z39.50 伺服器地址）（ISBN）（z39.50 伺服器輸出是否已是 utf-8 格式）
# $ python fetch_z3550.py library.cuhk.edu.hk 210 INNOPAC 9789863201915
# $ python fetch_z3550.py tulips.ntu.edu.tw 210 INNOPAC 9789863201915 --utf8
# yaz-client 192.83.186.170:210/INNOPAC

import abc


# --------------------------------------------------------- common routines

import sys
import re
import html.entities
from lxml import etree
from PyZ3950 import zoom
from pymarc import MARCReader, record_to_xml


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(html.entities.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is

    return re.sub("&#?\w+;", fixup, text)


xslRoot = etree.parse("./MARC21slim2MODS3-5.xsl")
transform = etree.XSLT(xslRoot)

conn = zoom.Connection(sys.argv[1], int(sys.argv[2]))
conn.databaseName = sys.argv[3]

query = zoom.Query('CCL', 'isbn=' + sys.argv[4])

res = conn.search(query)
try:
    print
    res[0].data
    conn.close()
    print
    "====================================="
    if "--utf8" in sys.argv:
        reader = MARCReader(res[0].data, to_unicode=True, force_utf8=True)

    else:
        reader = MARCReader(res[0].data)
    for record in reader:
        print(record)
        print
        "-------------------------------------"
        print
        unescape(etree.tostring(etree.fromstring(record_to_xml(record, namespace=True)), pretty_print=True))
        print
        "-------------------------------------"
        xmlRoot = etree.fromstring(record_to_xml(record, namespace=True))
        transRoot = transform(xmlRoot)
        print
        unescape(etree.tostring(transRoot, pretty_print=True))
        print
        "====================================="
except:
    print
    "no result"

if __name__ == '__main__':
    pass