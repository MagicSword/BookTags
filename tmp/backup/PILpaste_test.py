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

from PIL import Image

# --------------------------------------------------------- common routines



#開啟照片
imageA = Image.open('範例圖片C.jpg')
imageA = imageA.convert('RGBA')
widthA , heightA = imageA.size

#開啟簽名檔
imageB = Image.open('mySign.png')
imageB = imageB.convert('RGBA')
widthB , heightB = imageB.size

#重設簽名檔的寬為照片的1/2
newWidthB = int(widthA/2)
#重設簽名檔的高依據新的寬度等比例縮放
newHeightB = int(heightB/widthB*newWidthB)
#重設簽名檔圖片
imageB_resize = imageB.resize((newWidthB, newHeightB))

#新建一個透明的底圖
resultPicture = Image.new('RGBA', imageA.size, (0, 0, 0, 0))
#把照片貼到底圖
resultPicture.paste(imageA,(0,0))

#設定簽名檔的位置參數
right_bottom = (widthA - newWidthB, heightA - newHeightB)

#為了背景保留透明度，將im參數與mask參數皆帶入重設過後的簽名檔圖片
resultPicture.paste(imageB_resize, right_bottom, imageB_resize)

#儲存新的照片
resultPicture.save("已合成圖片.png")


if __name__ == '__main__':
    pass