# -*- coding: utf-8 -*-
from traceback import format_exc
import logging

from .entities import Record, ControlField, Field, SubField
from .errors import ReadingError, DecodingError, ValidationError

CHUNK_BLOCK = 2048
RECORD_END = b"\x1d"
ZONE_END = b"\x1e"
SUBZONE_START= b"\x1f"


def read_unimarc(filename):
    with open(filename, mode="rb") as flow:
        for idx,raw_record in enumerate(read_records(flow)):
            try:
                record = parse_record(raw_record, idx)
                record = decode_record(record, idx)
                yield record
            except Exception as exc:
                msg = "*"*20 + "ERROR WHILE READING RECORD #"+str(idx)+"\n"
                if isinstance(exc, (ReadingError, DecodingError,
                                    ValidationError)):
                    msg += str(exc)
                else:
                    msg += format_exc()
                if msg[-1] != "\n":
                    msg += "\n"
                logging.error(msg)


def read_records(bytes_flow):
    temp = bytes_flow.read(CHUNK_BLOCK)
    while True:
        char_idx = temp.find(RECORD_END)
        if char_idx != -1:
            raw_record = temp[:char_idx]
            temp = temp[char_idx+1:]
            yield raw_record
        else:
            temp += bytes_flow.read(CHUNK_BLOCK)
            if temp == b"":
                break


def parse_record(record, record_index):
    # Read label
    ctxt = ["Record #{}".format(record_index)]
    label = record[:24]
    if len(label) != 24:
        msg = _build_message("Label is shorter than expected",
                             data=record, context=ctxt)
        raise ReadingError(msg)
    record_obj = Record(label)
    # Read directory
    dir_end_char_idx = record.find(ZONE_END, 24)
    if dir_end_char_idx == -1:
        msg = _build_message("End of directory can't be detected",
                             data=record, context=ctxt)
        raise ReadingError(msg)
    directory = record[24:dir_end_char_idx]
    if len(directory) % 12 != 0 or len(directory) == 0:
        msg = _build_message("Directory can't be divided in 12-characters "
                             "segments", data=directory, context=ctxt)
        raise ReadingError(msg)
    if not directory.isdigit():
        msg = _build_message("Directory should only contain digits",
                             data=directory, context=ctxt)
        raise ReadingError(msg)
    # Extract fields metadata from directory
    fields_metadata = []
    char_idx = 0
    while char_idx < len(directory):
        tag, _ = _decode_value(directory[char_idx:char_idx+3])
        length = int(directory[char_idx+3:char_idx+7])
        start = int(directory[char_idx+7:char_idx+12])
        fields_metadata.append( (tag, start, length) )
        char_idx += 12
    # Extract fields data
    data = record[dir_end_char_idx+1:]
    exp_length = fields_metadata[-1][1] + fields_metadata[-1][2]
    if len(data) != exp_length:
        msg = _build_message("Data region doesn't have the expected length",
                             data=record, context=ctxt)
        raise ReadingError(msg)
    for field_idx, (tag, start, length) in enumerate(fields_metadata):
        ctxt.append("Zone #{} ({})".format(field_idx, repr(tag)))
        if data[start+length-1:start+length] != ZONE_END:
            msg = _build_message("Zone doesn't end with end-of-zone character",
                                 data=data[start:start+length], context=ctxt)
            raise ReadingError(msg)
        raw_field = data[start:start+length-1]
        if tag[:2] == "00":
            # Control field without subfields
            field = ControlField(tag, raw_field)
            record_obj.add_field(field)
        else:
            # Regular field
            if length < 2:
                msg = _build_message("Zone doesn't contain the indicators",
                                     data=raw_field, context=ctxt)
                raise ReadingError(msg)
            # Getting indicators
            indic0, i0_err_msg = _decode_value(
                raw_field[0:1], context=ctxt, name="First indicator")
            indic1, i1_err_msg = _decode_value(
                raw_field[1:2], context=ctxt, name="Second indicator")
            field = Field(tag, (indic0, indic1))
            for err_msg in (i0_err_msg, i1_err_msg):
                if err_msg is not None:
                    field.node_problems.append(err_msg)
            # Extracting sub-fields
            if raw_field[2:3] != SUBZONE_START:
                msg = _build_message("First sub-zone doesn't start with the "
                                     "start-of-sub-zone character",
                                     data=raw_field, context=ctxt)
                raise ReadingError(msg)
            sub_zone_idx = 0
            char_idx = 2
            while char_idx < len(raw_field):
                next_char_idx = raw_field.find(SUBZONE_START, char_idx+2)
                if next_char_idx == -1:
                    next_char_idx = len(raw_field)
                raw_sub_field = raw_field[char_idx+2:next_char_idx]
                if len(raw_sub_field) > 0:
                    ctxt.append("Sub-zone #{}".format(sub_zone_idx))
                    code, sub_err_msg = _decode_value(
                        raw_field[char_idx+1:char_idx+2], context=ctxt,
                        name="Sub-zone code")
                    sub_field = SubField(code, raw_sub_field)
                    if sub_err_msg is not None:
                        sub_field.node_problems.append(sub_err_msg)
                    field.add_sub_field(sub_field)
                    ctxt.pop()
                char_idx = next_char_idx
                sub_zone_idx += 1
            record_obj.add_field(field)
        ctxt.pop()
    return record_obj


def decode_record(record, record_index, default_encoding="utf-8"):
    ctxt = ["Record #{}".format(record_index)]
    # Get process data (zone "100" / sub-zone "a")
    flds = record.fields("100")
    if len(flds) == 0:
        msg = _build_message(
            "Record does not contain the mandatory \"100\" zone; trying the "
            "default encoding to decode the textual values", context=ctxt)
        record.node_problems.append(msg)
        logging.error(msg)
        encoding = default_encoding
    else:
        if len(flds) > 1:
            msg = _build_message(
                "Record contains more than one \"100\" zone; working with "
                "first one", context=ctxt)
            record.node_problems.append(msg)
            logging.error(msg)
        field = flds[0]
        ctxt.append("Zone \"100\"")
        sub_flds = field.sub_fields("a")
        if len(sub_flds) == 0:
            msg = _build_message(
                "Zone does not contain the mandatory \"a\" sub-zone; trying "
                "the default encoding to decode the textual values",
                context=ctxt)
            field.node_problems.append(msg)
            logging.error(msg)
            encoding = default_encoding
        else:
            if len(sub_flds) > 1:
                msg = _build_message(
                    "Zone contains more than one \"a\" sub-zone; working with "
                    "first one", context=ctxt)
                field.node_problems.append(msg)
                logging.error(msg)
            sub_field = sub_flds[0]
            ctxt.append("Sub-zone \"a\"")
            # CMARC tag 100 length 35
            if len(sub_field.value) != 35:
                msg = _build_message(
                    "Value doesn't have the expected length (35)",
                    data=sub_field.value, context=ctxt)
                sub_field.node_problems.append(msg)
                logging.warning(msg)
            char_set = sub_field.value[26:28]
            if char_set != b"50":
                msg = _build_message(
                    "Record uses a character set that is not addressed; trying "
                    "the default encoding to decode the textual values",
                    data=char_set, context=ctxt[:1])
                record.node_problems.append(msg)
                logging.warning(msg)
                encoding = default_encoding
            else:
                encoding = "utf-8"
            ctxt.pop()
        ctxt.pop()
    # Decode record contents (using utf-8 encoding)
    val, err_msg = _decode_value(record.label, encoding=encoding,
                                 context=ctxt, name="Label")
    record.label = val
    if err_msg is not None:
        record.node_problems.append(err_msg)
    ctxt.pop()
    for fld_idx, field in enumerate(record.fields()):
        ctxt.append("Zone #{} (\"{}\")".format(fld_idx,field.name))
        if isinstance(field, ControlField):
            val, err_msg = _decode_value(field.value, encoding=encoding,
                                         context=ctxt, name="Textual value")
            field.value = val
            if err_msg is not None:
                field.node_problems.append(err_msg)
        else:
            for sub_idx, sub_field in enumerate(field.sub_fields()):
                ctxt.append("Sub-zone #{} (\"{}\")"
                            "".format(sub_idx, sub_field.name))
                val, err = _decode_value(sub_field.value, encoding=encoding,
                                         context=ctxt, name="Textual value")
                sub_field.value = val
                if err_msg is not None:
                    sub_field.node_problems.append(err_msg)
                ctxt.pop()
        ctxt.pop()
    return record


def _decode_value(raw_value, encoding="646", raise_exception=False,
                  context=None, name=None):
    error_msg = None
    try:
        value = raw_value.decode(encoding)
    except UnicodeDecodeError as exc:
        if name is not None:
            ctxt = context.copy() if context is not None else []
            ctxt.append(name)
        else:
            ctxt = context
        error_msg = _build_message("Error while decoding bytes sequence:\n{}"
                                   "".format(str(exc)),
                                   context=ctxt, data=raw_value)
        if raise_exception:
            raise DecodingError(error_msg)
        else:
            logging.warning(error_msg)
            value = raw_value.decode(encoding, "backslashreplace")
    return value, error_msg

def _build_message(message, context=None, data=None):
    msg = ""
    if context is not None:
        msg += "{}\n".format(" / ".join(context))
    msg += message
    if data is not None:
        msg += "\nRelated data:\n{}".format(repr(data))
    return msg
