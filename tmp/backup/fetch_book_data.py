#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Name of this command

DESCRIPTION here

"""
__all__ = ['help']
__author__ = "Nero <magicsword@gmail.com>"
__date__ = "26 February 2001"
__copyright__ = "Copyright 2017, The Nostalgic project"
__license__ = "MPL 2.0"
__version__ = "0.1.0"
__maintainer__ = "Nero"
__status__ = "Dev"
__credits__ = """Bleo, bleo bleo blue.
Bleo, bleo bleo blue.
"""

# Known bugs that can't be fixed here:
#   - synopsis() cannot be prevented from clobbering existing
#     loaded modules.
#   - If the __file__ attribute on a module is a relative path and
#     the current directory is changed with os.chdir(), an incorrect
#     path will be displayed.

import abc

# --------------------------------------------------------- common routines

import sys
import re, htmlentitydefs
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
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
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