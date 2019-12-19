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
import logging
from datetime import datetime

from . import Project_HOME


# --------------------------------------------------------- common routines
log_path = os.path.join(Project_HOME, "logs")
filename = f"{datetime.now().strftime('%Y%m%d-%H%M')}.log"

def create_logger(log_folder):
    logging.captureWarnings(True)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    my_logger = logging.getLogger('py.warnings')
    my_logger.setLevel(logging.INFO)

    if not log_folder:
        log_path_finall = log_path
    else:
        log_path_finall = os.path.join(log_path,log_folder)

    # print(f"log_path:{log_path_finall}")

    os.makedirs(log_path_finall, exist_ok=True)

    # if not os.path.exists(log_path+log_folder):
    #     os.makedirs(os.path.join(log_path+log_folder))

    log_filename = os.path.join(log_path_finall, filename)
    print(f"log_filename:{log_filename}")

    fileHandler = logging.FileHandler(log_filename, mode='a', encoding='utf-8', delay=False)
    fileHandler.setFormatter(formatter)
    my_logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(formatter)
    my_logger.addHandler(consoleHandler)

    return my_logger


if __name__ == '__main__':
    pass