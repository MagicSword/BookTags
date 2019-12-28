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

# --------------------------------------------------------- common routines

import sys
import inspect

from . import *


def main():
    crawler = [
        m[0]
        for m in inspect.getmembers(sys.modules[__name__], inspect.isclass)
        if m[1].__module__.startswith("crawlers") and m[0] == sys.argv[1]
    ]
    if len(crawler):
        filename = crawler[0].lower().replace("crawler", "")

        Crawler = eval(crawler[0])
        c = Crawler()
        c.get_books()
        c.export("data/{}_events.json".format(filename))
    else:
        print("Crawler not found!")


if __name__ == "__main__":
    main()