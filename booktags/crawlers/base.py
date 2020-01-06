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

import requests
from bs4 import BeautifulSoup


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

    def get_book(self):
        pass

    def export(self, filename):
        # v = BookValidator(schema)
        # for book in self.books:
        #     v.validate(book)
        #     if v.errors:
        #         for key, val in v.errors.items():
        #             print("{} - {}: {}".format(book["name"], key, val))

        with open(filename, "w") as f:
            f.write(json.dumps(self.books, indent=4, sort_keys=True))

    def get_soup(self, url: str) -> object:
        """

        :param url:
        :return: soup
        """
        # url = f"{self.base_domain}/products/{url}"


        try:
            res = requests.get(url)
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

        # TODO : functional programming or?
        # self.cur_soup = soup
        return soup