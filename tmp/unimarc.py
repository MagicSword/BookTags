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
# https://gist.github.com/isergey/1051026
import abc

from pymarc import Record
# --------------------------------------------------------- common routines



class UnimarcRecord(Record):
    def __init__(self, *args, **kwargs):
        super(UnimarcRecord, self).__init__(*args, **kwargs)


    def decode_marc(self, marc, to_unicode=False, force_utf8=False, encoding=None,
                    hide_utf8_warnings=False, utf8_handling='strict'):
        """
        decode_marc() accepts a MARC record in transmission format as a
        a string argument, and will populate the object based on the data
        found. The Record constructor actually uses decode_marc() behind
        the scenes when you pass in a chunk of MARC data to it.
        """
        # extract record leader
        self.leader = marc[0:LEADER_LEN]
        if len(self.leader) != LEADER_LEN:
            raise RecordLeaderInvalid

        # extract the byte offset where the record data starts
        base_address = int(marc[12:17])
        if base_address <= 0:
            raise BaseAddressNotFound
        if base_address >= len(marc):
            raise BaseAddressInvalid

        # extract directory, base_address-1 is used since the
        # director ends with an END_OF_FIELD byte
        directory = marc[LEADER_LEN:base_address - 1]

        # determine the number of fields in record
        if len(directory) % DIRECTORY_ENTRY_LEN != 0:
            raise RecordDirectoryInvalid
        field_total = len(directory) / DIRECTORY_ENTRY_LEN

        # add fields to our record using directory offsets
        field_count = 0
        while field_count < field_total:
            entry_start = field_count * DIRECTORY_ENTRY_LEN
            entry_end = entry_start + DIRECTORY_ENTRY_LEN
            entry = directory[entry_start:entry_end]
            entry_tag = entry[0:3]
            entry_length = int(entry[3:7])
            entry_offset = int(entry[7:12])
            entry_data = marc[base_address + entry_offset:
            base_address + entry_offset + entry_length - 1]

            # assume controlfields are numeric; replicates ruby-marc behavior
            if entry_tag < '010' and entry_tag.isdigit():
                field = Field(tag=entry_tag, data=entry_data)
            elif entry_tag[0] == '4':
                subfields = list()
                subs = entry_data.split(SUBFIELD_INDICATOR)
                first_indicator = subs[0][0]
                second_indicator = subs[0][1]
                field_data = subs[1:]
                i = 0
                field_data_len = len(field_data)
                while i < field_data_len:
                    #if subfield 1, then read embedded field tag number
                    if field_data[i][0] == '1':
                        embedded_field_tag = field_data[i][1:4]
                        embedded_field_i1 = field_data[i][4]
                        embedded_field_i2 = field_data[i][5]

                        embedded_subfields = list()
                        i += 1
                        while i < field_data_len and field_data[i][0] != '1':
                            code = field_data[i][0]
                            data = field_data[i][1:]

                            if to_unicode:
                                if self.leader[9] == 'a' or force_utf8:
                                    data = data.decode('utf-8', utf8_handling)
                                elif encoding and (encoding != 'marc-8'):
                                    data = data.decode(encoding, utf8_handling)
                                else:
                                    data = marc8_to_unicode(data, hide_utf8_warnings)
                            embedded_subfields.append(code)
                            embedded_subfields.append(data)
                            i += 1

                        emb_field = Field(tag=embedded_field_tag,
                                          indicators=[embedded_field_i1, embedded_field_i2],
                                          subfields=embedded_subfields)
                        subfields.append('1')
                        subfields.append(emb_field)

                field = Field(
                    tag=entry_tag,
                    indicators=[first_indicator, second_indicator],
                    subfields=subfields,
                    )

            else:
                subfields = list()
                subs = entry_data.split(SUBFIELD_INDICATOR)
                first_indicator = subs[0][0]
                second_indicator = subs[0][1]
                for subfield in subs[1:]:
                    if len(subfield) == 0:
                        continue
                    code = subfield[0]
                    data = subfield[1:]

                    if to_unicode:
                        if self.leader[9] == 'a' or force_utf8:
                            data = data.decode('utf-8', utf8_handling)
                        elif encoding and (encoding != 'marc-8'):
                            data = data.decode(encoding, utf8_handling)
                        else:
                            data = marc8_to_unicode(data, hide_utf8_warnings)
                    subfields.append(code)
                    subfields.append(data)
                field = Field(
                    tag=entry_tag,
                    indicators=[first_indicator, second_indicator],
                    subfields=subfields,
                    )

            self.add_field(field)
            field_count += 1

        if field_count == 0:
            raise NoFieldsFound

