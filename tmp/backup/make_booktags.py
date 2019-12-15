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

import abc

# --------------------------------------------------------- common routines










from PIL import Image, ImageDraw, ImageFont
font = ImageFont.truetype( "C:\\Windows\\Fonts\\cwTeXQYuan-Medium.ttf", 40 )
im = Image.new( "RGB", (228,228) ,color=(255,255,255))
draw = ImageDraw.Draw( im )
draw.ink = 0
text = "最後一個知\n   300\n   3441\n   2017"
draw.multiline_text((5,5), text, fill=None, font=font, anchor=None, spacing=1, align="center")
im.save( "text.jpg" )




if __name__ == '__main__':
    pass