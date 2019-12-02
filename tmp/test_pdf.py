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

from reportlab.pdfgen.canvas import Canvas
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('cwTeXQHeiBd', 'C:/Windows/Fonts/cwTeXQHei-Bold.ttf'))

canvas = Canvas('test_pdf.pdf')

canvas.setFont('cwTeXQHeiBd', 32)
canvas.drawString(10, 150, "最後一個知   300   3441   2017")
canvas.drawString(10, 100, "中文許功蓋，測試")
canvas.drawString(100, 300, u'最後一個知   300   3441   2017')


def forms(canvas):
 #first create a form...
 canvas.beginForm("SpumoniForm")
 #re-use some drawing functions from earlier
 spumoni(canvas)
 canvas.endForm()
 #then draw it
 canvas.doForm("SpumoniForm")




canvas.save()

if __name__ == '__main__':
    pass