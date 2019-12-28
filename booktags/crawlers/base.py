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

import json
from datetime import datetime
from cerberus import Validator


# --------------------------------------------------------- common routines

class BookValidator(Validator):
    # def _validate_is_date(self, is_date, field, value):
    #     """Test if a date is valid.
    #     The rule's arguments are validated against this schema:
    #     {'type': 'boolean'}
    #     """
    #     if is_date:
    #         valid = True
    #         try:
    #             this_date = datetime.datetime.strptime(value, "%Y-%m-%d")
    #         except:
    #             valid = False
    #         if not valid:
    #             self._error(field, "must be valid date")
    pass



class BaseCrawler(object):
    def __init__(self):
        self.books = []

    def get_books(self):
        pass

    def export(self, filename):
        v = BookValidator(schema)
        for book in self.books:
            v.validate(book)
            if v.errors:
                for key, val in v.errors.items():
                    print("{} - {}: {}".format(book["name"], key, val))

        with open(filename, "w") as f:
            f.write(json.dumps(self.books, indent=4, sort_keys=True))