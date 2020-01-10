# -*- coding: utf-8 -*-

from .tree_utils import ValueNode, ParentNode


class Record(ParentNode):
    def __init__(self, label):
        super().__init__("RECORD")
        self.label = label

    def get_values(self, tag, code):
        values = []
        for field in self.fields(tag):
            if isinstance(field, ControlField):
                values.append(field.value)
            else:
                for sub_field in field.sub_fields(code):
                    values.append(sub_field.value)
        return values

    def get_value(self, tag, code):
        for field in self.fields(tag):
            if isinstance(field, ControlField):
                return field.value
            for sub_field in field.sub_fields(code):
                return sub_field.value
        return None

    def fields(self, tag=None):
        return self._get_children(tag)

    def add_field(self, field):
        self._add_child(field)

    def __str__(self):
        pbs = self.problems
        if len(pbs) == 0:
            pb_msg = ""
        else:
            pb_msg = "problems:\n"
            for pb in pbs:
                pb_msg += "  "
                pb_msg += pb.replace("\n", "\n  ")
                if pb_msg[-1] != "\n":
                    pb_msg += "\n"
        return ("RECORD\n{}label: {}\nfields:\n{}\n"
                "".format(pb_msg, repr(self.label),
                          "\n".join(str(fld) for fld in self.fields())))

class ControlField(ValueNode):
    def __init__(self, tag, value):
        super().__init__("CONTROL FIELD", value)
        self.tag = tag

    @property
    def name(self):
        return self.tag

    def __str__(self):
        return "    {}    {}".format(self.tag, repr(self.value))

    
class Field(ParentNode):
    def __init__(self, tag, indicators):
        super().__init__("FIELD")
        self.tag = tag
        self.indicators = indicators

    @property
    def name(self):
        return self.tag

    def sub_fields(self, code=None):
        return self._get_children(code)

    def add_sub_field(self, sub_field):
        self._add_child(sub_field)

    def __str__(self):
        return ("{},{} {} {}".format(
            self.indicators[0], self.indicators[1], self.tag,
            "\n        ".join(str(fld) for fld in self.sub_fields())))


class SubField(ValueNode):
    def __init__(self, code, value):
        super().__init__("SUB-FIELD", value)
        self.code = code

    @property
    def name(self):
        return self.code

    def __str__(self):
        return "{}  {}".format(self.code, repr(self.value))

