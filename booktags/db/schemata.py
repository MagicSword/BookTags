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

import copy


# --------------------------------------------------------- common routines


ThingSchema = {
    "name": {"type": "string", "required": True, "nullable": True},
    "url": {"type": "string", "required": True, "nullable": True},
    "image": {"type": "string", "required": True, "nullable": True},
    "identifier": {"type": "string", "required": True, "nullable": True},
    "description": {"type": "string", "required": True, "nullable": True},
    "alternateName": {"type": "string", "required": True, "nullable": True},
    "width" : {"type": "float", "required": True, "nullable": True},
    "height": {"type": "float", "required": True, "nullable": True},
    "depth" : {"type": "float", "required": True, "nullable": True},
    "weight": {"type": "float", "required": True, "nullable": True}
}

CreativeWorkSchema = copy.deepcopy(ThingSchema)
CreativeWorkSchema.update({
    "about":  {"type": "string", "required": True, "nullable": True},
    "abstract":  {"type": "string", "required": True, "nullable": True},
    "author":  {"type": "string", "required": True, "nullable": True},
    "locationCreated":  {"type": "string", "required": True, "nullable": True},
    "contentRating":  {"type": "string", "required": True, "nullable": True},
    "datePublished":  {"type": "date", "required": True, "nullable": True},
    "genre":  {"type": "string", "required": True, "nullable": True},
    "inLanguage":  {"type": "string", "required": True, "nullable": True},
    "keywords":  {"type": "string", "required": True, "nullable": True},
    "publisher":  {"type": "string", "required": True, "nullable": True},
    "review":  {"type": "string", "required": True, "nullable": True},
    "comment":  {"type": "string", "required": True, "nullable": True},
    "translationOfWork":  {"type": "string", "required": True, "nullable": True},
    "translator":  {"type": "string", "required": True, "nullable": True},
    "workTranslation":  {"type": "string", "required": True, "nullable": True}
})

BookSchema = copy.deepcopy(CreativeWorkSchema)
BookSchema.update({
"bookEdition" : {"type": "string", "required": True, "nullable": True},
"bookFormation" : {"type": "string", "required": True, "nullable": True},
"illustrator" : {"type": "string", "required": True, "nullable": True},
"isbn" : {"type": "string", "required": True, "nullable": True},
"numberOfPages" : {"type": "integer", "required": True, "nullable": True},
# addition
"locationPublished":  {"type": "string", "required": True, "nullable": True},
# name = title + subtitle
"title": {"type": "string", "required": False, "nullable": True},
"title_english": {"type": "string", "required": False, "nullable": True},
"subtitle": {"type": "string", "required": False, "nullable": True},
"price": {"type": "integer", "required": False, "nullable": True},
"series": {"type": "string", "required": False, "nullable": True},
"summary": {"type": "string", "required": False, "nullable": True},
"summaryAuthor": {"type": "string", "required": False, "nullable": True},
"toc": {"type": "string", "required": False, "nullable": True}
})


StoreBookSchema = copy.deepcopy(BookSchema)
StoreBookSchema.update({
    "discountPrice" : {"type": "integer", "required": False, "nullable": True},
    "discountRate" : {"type": "float", "required": False, "nullable": True},
    "discountDate" : {"type": "date", "required": False, "nullable": True},
    "category" : {"type": "list", "required": False, "nullable": True},
    "paperSize" : {"type": "string", "required": False, "nullable": True},
    "printingColor" : {"type": "string", "required": False, "nullable": True}
})


LibraryBookSchema = copy.deepcopy(BookSchema)
LibraryBookSchema.update({
    "num_category": {"type": "string", "required": False, "nullable": True},
    "num_author": {"type": "string", "required": False, "nullable": True},
    "keepsite": {"type": "string", "required": False, "nullable": True},
    "numberOfCopies": {"type": "string", "required": False, "nullable": True}
})




# 平裝 / 336頁 / 25k正 / 14.8 x 21 cm / 普通級 / 單色印刷 / 初版


if __name__ == '__main__':
    pass