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
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
stylesheet=getSampleStyleSheet()
normalStyle = stylesheet['Normal']

import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('cwTeXQHeiBd', 'C:/Windows/Fonts/cwTeXQHei-Bold.ttf'))

import re
import pandas as pd
import numpy as np
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    filename='simple_table_grid_log.txt')


# container for the 'Flowable' objects


# P0 = Paragraph('''
#     <b>A pa<font color=red>r</font>a<i>graph</i></b>
#     <super><font color=yellow>1</font></super>''',
#     stylesheet["Normal"])
#
# P1 = Paragraph('''
#     The <b>ReportLab Left
#     <font color=red>Logo</font></b>
#     Image''',
#     stylesheet["Normal"])
#
# P2 = Paragraph('''
#     最後一個知 300 3441 2017
#     ''',
#     stylesheet["Normal"])

# data = [['最後一個知\n300\n3441\n2017', '11', '12', '13', '14','15','16','17', '18', '19', '10', '1A','1B','1C','1D'],
#         ['20', '21', '22', '23', '24','25','26','27', '28', '29', '20', '2A','2B','2C','2D'],
#         ['30', '31', '32', '33', '34','35','36','37', '38', '39', '30', '3A','3B','3C','3D'],
#         ['40', '41', '42', '43', '44','45','46','47', '48', '49', '40', '4A','4B','4C','4D'],
#         ['50', '51', '52', '53', '54','55','56','57', '58', '59', '50', '5A','5B','5C','5D'],
#         ['60', '61', '62', '63', '64','65','66','67', '68', '69', '60', '6A','6B','6C','6D'],
#         ['70', '71', '72', '73', '74','75','76','77', '78', '79', '70', '7A','7B','7C','7D'],
#         ['80', '81', '82', '83', '84','85','86','87', '88', '89', '80', '8A','8B','8C','8D'],
#         ['90', '91', '92', '93', '94','95','96','97', '98', '99', '90', '9A','9B','9C','9D'],
#         ['A0', 'A1', 'A2', 'A3', 'A4','A5','A6','A7', 'A8', 'A9', 'A0', 'AA','AB','AC','AD']
#         ]

# ------------------------ char width

widths = [
    (126,    1), (159,    0), (687,     1), (710,   0), (711,   1),
    (727,    0), (733,    1), (879,     0), (1154,  1), (1161,  0),
    (4347,   1), (4447,   2), (7467,    1), (7521,  0), (8369,  1),
    (8426,   0), (9000,   1), (9002,    2), (11021, 1), (12350, 2),
    (12351,  1), (12438,  2), (12442,   0), (19893, 2), (19967, 1),
    (55203,  2), (63743,  1), (64106,   2), (65039, 1), (65059, 0),
    (65131,  2), (65279,  1), (65376,   2), (65500, 1), (65510, 2),
    (120831, 1), (262141, 2), (1114109, 1),
]

def get_width( o ):
    """Return the screen column width for unicode ordinal o."""
    # http://www.unicode.org/Public/4.0-Update/EastAsianWidth-4.0.0.txt
    # http://www.unicode.org/reports/tr44/tr44-4.html

    global widths
    if o == 0xe or o == 0xf:
        return 0
    for num, wid in widths:
        if o <= num:
            return wid
    return 1


def get_title_head(in_string):
    """get title head
    Unicode : 3mm , Ascii : 2mm
    param : string
    return : first 18mm string
    """
    out_string = " "
    count = 0
    for char in in_string:

        char_width = get_width(ord(char))

        if char_width == 2:
            count = count + 3
            out_string += char
        elif char_width == 1:
            count = count + 2
            out_string += char
        else:
            pass



        if count >= 15:
            print("Count: {:02d} - {}".format(count, out_string))
            return out_string + " "
    print("Count: {:02d} - {}".format(count, out_string))
    return out_string + " "





def cjk_detect(title):
    # korean
    texts = title[:10]
    if re.search("[\uac00-\ud7a3]", texts):
        return "ko"
    # japanese
    if re.search("[\u3040-\u30ff]", texts):
        return "ja"
    # chinese
    if re.search("[\u4e00-\u9FFF]", texts):
        return "zh"
    return 'en'

def get_head5(encoding):
    if cjk_detect(encoding) == 'en':
        ans = encoding[:8]
    else:
        ans = encoding[:5]
    return ans

# ------------------------- char width

def get_df(filename,DELETE,REPRINT_ONLY):
    """

    :param filename:
    id	isbn	title	catalogue	cutter	pub_date	copy_info	fail	note	reprint	delete	location
    :return: 15:10 df
    """
    tags_list = []
    df_read = pd.read_csv(filename)
    # remove missing values
    df_csv = df_read.fillna(value="")
    for index, row in df_csv.iterrows():
        # print("{} - {}".format(row['title'], row['callnumber']))
        # print(row['callnumber'])
        # print(row['id'])
        # tag 輸出 四行，一行10 char, 五中文字
        # 第一行： 中文書名，五個字
        # 第二行： 索書號 - 分類號
        # 第三行： (6 - 3) 前 6 作者名四角號碼，後3 序號
        # 第四行： 原 索書號 第四行

        # 刪掉 delete row
        if DELETE == True and row['delete'] == "delete":
            continue

        if REPRINT_ONLY == True and row['reprint'] != 'reprint':
            continue





        #if row['reprint'] == 'reprint':
        if True:
            id = row['id']
            # TODO: 中文取5個字，英文取 10 char , 中英混合？
            # title
            title = get_title_head(row['title_short'])
            catalogue = row['catalogue']
            cutter = row['cutter']
            pub_date = row['pub_date']
            copy_info = row['copy_info']

            # if len(tmp[1]) > 6:
            #     tmp_line = "{}-{:03d}".format(tmp[1][:6],int(id))
            # else:
            #     tmp_line = "{}-{:03d}".format(tmp[1], int(id))
            # tmp_line = tmp_line[:10]
            # if len(tmp) > 3:
            #     callnumber = "{}\n{}\n{}".format( tmp[0],tmp_line,tmp[2])
            # else:
            #     tmp[1] = tmp_line
            #     callnumber = "\n".join(tmp)
            #print("{}: {} - {}".format(index, "----", callnumber))
            if copy_info == 'nan' or copy_info == '':
                tags = "{0}\n{1}\n{2}-{3}\n{4}".format(title, catalogue, cutter, id, pub_date)
            else:
                tags = "{0}\n{1}\n{2}-{3}\n{4}-{5}".format(title, catalogue, cutter, id, pub_date, copy_info)

            tags_list.append(tags)
        else:
            continue

    return tags_list

def make_pdf(array,page_num,row,col):
    """

    :return:
    """
    import time

    timestr = time.strftime("%m%d%H%M")
    table_format = "{}x{}".format(row,col)
    name_base = "BookTags{}_{}".format(table_format,timestr)
    name_ext = "pdf"

    for i in range(page_num):
        filename = "{}-p{:02d}.{}".format(name_base,i,name_ext)

        doc = SimpleDocTemplate(filename, pagesize=(A4[1], A4[0]),
                            topMargin=0.2 * cm,
                            bottomMargin=0.2 * cm,
                            leftMargin=0.2 * cm,  #0.85
                            rightMargin=0.2 * cm, #0.85
                            showBoundary=False
                            )
        tab = Table(array[i], col * [2.0 * cm], row * [2.0 * cm])
        tab.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black, None, (2, 2, 1)),
            ('FONTSIZE', (0, 0), (-1, -1), 11),   # Fontsize   1 point = 0.352 mm
            ('FONT', (0, 0), (-1, -1), 'cwTeXQHeiBd'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black, None, (2, 2, 1))
        ]))

        elements = []
        elements.append(tab)
        # write the document to disk
        doc.build(elements)
        print("Saving:{}".format(filename))



def format_tags(ele,row,col):
    """ tags list format

    :param element:
    :return:
    """
    # data[page][row][col]

    ele_num = len(ele)
    page_num = (ele_num // (row * col)) + 1

    # create empty str list
    tmp_list = ["" for x in range(page_num * row * col)]
    # fill element into tmp_list
    for i in range(ele_num):
        tmp_list[i] = ele[i]

    # ndarray.resize() fill 0
    # np.resize() fill origin element
    # new_array = np.resize(ele, (page_num, row, col))
    #
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.resize.html
    # numpy.resize(a, new_shape)
    # Return a new array with the specified shape.
    #
    # If the new array is larger than the original array, then the new array is filled
    # with repeated copies of a. Note that this behavior is different from a.resize(new_shape)
    # which fills with zeros instead of repeated copies of a.

    new_array = np.resize(tmp_list,(page_num, row, col))
    new_list = new_array.tolist()
    #logging.info("type new_list : {}".format(type(new_list)))
    return (page_num,new_list)

def cli():
    """

    :return:
    """
    filename = "E:/_Documents/GitHub/PyCharm_Workspace/BookTags/tmp/bookshelf_callnumber_308.csv"
    # 需要去掉的欄位
    # delete :
    # reprint :

    # 去掉錯誤記錄
    DELETE = True
    # 只印新紀錄
    REPRINT_ONLY = True


    tags = get_df(filename,DELETE,REPRINT_ONLY)

    page_num,new_tags = format_tags(tags,10,14)
    make_pdf(new_tags,page_num,10,14)



if __name__ == '__main__':
    cli()