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

from PyZ3950 import zoom


# --------------------------------------------------------- common routines
# http://metadata.ncl.edu.tw/blstkm/htm/z39.50.htm
domain="metadata.ncl.edu.tw"
port=210
dbname="bg"
record_format="MARC21"
encoding="utf-8"


# conn = zoom.Connection(domain, port)
# conn.databaseName = dbname
# conn.preferredRecordSyntax = record_format
# query = zoom.Query('CCL', 'nb="9789864341313"')
# res = conn.search(query)
# for r in res:
#     print(str(r))
#
# conn.close()

from PyZ3950 import zoom

conn = zoom.Connection ('192.83.186.170', 210)
conn.databaseName = 'INNOPAC'
conn.preferredRecordSyntax = 'MARC21'

query = zoom.Query ('CCL', 'isbn="9789864341313"')

res = conn.search (query)
print(res[0])

conn.close ()


if __name__ == '__main__':
    pass