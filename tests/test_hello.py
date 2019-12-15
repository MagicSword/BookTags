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

import unittest


# --------------------------------------------------------- common routines

class TestAddition(unittest.TestCase):
    def setUP(selfs):
        print("Setting up the test")
    def tearDown(self):
        print("Tearing down the test")
    def test_twoPlusTwo(self):
        total = 2 + 2
        self.assertEqual(4,total)




if __name__ == '__main__':
    unittest.main()