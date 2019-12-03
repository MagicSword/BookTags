#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    example.py
    ~~~~~~~~~
    A simple command line application to run flask apps.
    :copyright: http://blog.changyy.org/2010/09/python-marc21-iso-2709.html
    :license: BSD-3-Clause
"""

# Known bugs that can't be fixed here:
#   - synopsis() cannot be prevented from clobbering existing
#     loaded modules.
#   - If the __file__ attribute on a module is a relative path and
#     the current directory is changed with os.chdir(), an incorrect
#     path will be displayed.
#

import abc


# --------------------------------------------------------- common routines

class MARC(object):
    """
    MARC class

    使用方式：
    marc = MARC( [target_file] )
    for rawdata in marc.get_raw_entries():
        tmp = None
        value , tmp = marc.get_field_value( rawdata , 'FIELD_ID' , tmp )
        if len(value) > 0:
            for raw in re.findall( marc.RE_FIELD_DATA , value[0] ):
                print raw
                break

    """
    def __init__(self, file_list=[]):
        self.file_list = file_list if file_list is not None and len(file_list) > 0 else []
        self.fd = None
        self.RE_FIELD_DATA = re.compile('\x1f.([^\x1e\x1f]+)')

    def get_raw_entries(self, cnt=None):
        out = []
        cnt = int(cnt) if cnt is not None else 0
        while True:
            if self.fd is None:
                if self.file_list is None or len(self.file_list) == 0:
                    return out
                try:
                    self.fd = open(self.file_list[0], 'rb')
                    self.file_list = self.file_list[1:]
                except Exception as inst:
                    print
                    inst
                    return out
            try:
                header = self.fd.read(24)

                if not header:  # EOF
                    self.fd.close()
                    self.fd = None
                else:
                    record_size = int(header[0:5])
                    record_data = self.fd.read(record_size - 24)
                    out.append(header + record_data)
            except Exception as inst:
                print
                inst
                return out

            if cnt != 0 and len(out) == cnt:
                return out

    def get_field_value(self, rawdata, field, dictField=None):
        if dictField is None:

            header = rawdata[0:24]
            field_length = int(header[20:21])
            field_offset = int(header[21:22])
            data_begin_offset = int(header[12:17])
            raw_field_info = rawdata[24:data_begin_offset - 1]  # skip field end delimiter

            dictField = {}
            for i in range(0, len(raw_field_info), 12):
                begin = i
                end = i + 3
                sub_field_name = raw_field_info[begin: end]

                begin = end
                end = begin + field_length
                sub_field_data_length = raw_field_info[begin: end]

                begin = end
                end = begin + field_offset
                sub_field_data_offset = raw_field_info[begin: end]

                if sub_field_name not in dictField:
                    dictField[sub_field_name] = []
                raw_value = [int(sub_field_data_length), int(sub_field_data_offset) + data_begin_offset]
                dictField[sub_field_name].append(raw_value)

        out = []
        if field is not None and field in dictField:
            for data_length_and_offset in dictField[field]:
                out.append(rawdata[data_length_and_offset[1]: data_length_and_offset[0] + data_length_and_offset[1]])

        return (out, dictField)


def pre_process():
    target = 'I:\\_Downloads\\output3.iso'
    f = open(target, 'rb')
    rec_cnt = 0
    total_size = 0
    print
    "### 012345678901234567890123 ###"
    while True:
        header = f.read(24)
        total_size = total_size + len(header)
        if not header:
            break

        record_size = int(header[0:5])
        record_data = f.read(record_size - 24)

        total_size = total_size + len(record_data)
        rec_cnt = rec_cnt + 1

        print
        "---", header, "---", record_size
        if False:
            o = open('test.marc' + str(rec_cnt), 'wb')
            o.write(header)
            o.write(record_data)
            o.close()
        # print record_data

    print
    "Total:", total_size, ", Record Cnt:", rec_cnt
    f.close

def getFieldValue(rawdata, field=None, dictField=None):
    """
    get Field Value

    用法：
    tmp = None
    value , tmp = getFieldValue( rawdata , '003' , tmp )
    value , tmp = getFieldValue( rawdata , '005' , tmp )
    ...
    其中 rawdata 是完整的資料，包括 header + dinctionary + data 三部分；
    value 是一個 array ，因為有些指定的 field name 可能出現多次，所以就用 array 記錄；
    tmp 是用來暫存 dictionary 資料，可以省下重新處理來增加效率的

    :param rawdata:
    :param field:
    :param dictField:
    :return:
    """
    if dictField is None:

        header = rawdata[0:24]
        field_length = int(header[20:21])
        field_offset = int(header[21:22])
        data_begin_offset = int(header[12:17])
        raw_field_info = rawdata[24:data_begin_offset - 1]  # skip field end delimiter

        dictField = {}
        for i in range(0, len(raw_field_info), 12):
            begin = i
            end = i + 3
            sub_field_name = raw_field_info[begin: end]

            begin = end
            end = begin + field_length
            sub_field_data_length = raw_field_info[begin: end]

            begin = end
            end = begin + field_offset
            sub_field_data_offset = raw_field_info[begin: end]

            if sub_field_name not in dictField:
                dictField[sub_field_name] = []
            dictField[sub_field_name].append(
                [int(sub_field_data_length), int(sub_field_data_offset) + data_begin_offset])

    out = []
    if field is not None and field in dictField:
        # print dictField[field]
        for data_length_and_offset in dictField[field]:
            out.append(rawdata[data_length_and_offset[1]: data_length_and_offset[0] + data_length_and_offset[1]])

    return (out, dictField)


if __name__ == '__main__':
    pass