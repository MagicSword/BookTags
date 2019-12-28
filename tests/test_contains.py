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

import abc


# --------------------------------------------------------- common routines


from tests.contains import contains
from ward import expect, test


@test("contains returns True when item is in list")
def _():
    list_of_ints = list(range(100000))
    result = contains(list_of_ints, 5)
    expect(result).equals(True)

@test("1 plus 2 equals 3")
def _():
    expect(1 + 2).equals(3)

if __name__ == '__main__':
    pass