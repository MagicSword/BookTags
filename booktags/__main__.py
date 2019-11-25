#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    __main__.py
    ~~~~~~~~~
    __main__
    :copyright: 2019 Miller
    :license: BSD-3-Clause
"""

# Known bugs that can't be fixed here:
#   - synopsis() cannot be prevented from clobbering existing
#     loaded modules.
#   - If the __file__ attribute on a module is a relative path and
#     the current directory is changed with os.chdir(), an incorrect
#     path will be displayed.

from __future__ import absolute_import

# --------------------------------------------------------- common routines


__all__ = ("main",)


def main():
    from booktags.cli import cli

    cli()


if __name__ == "__main__":
    main()