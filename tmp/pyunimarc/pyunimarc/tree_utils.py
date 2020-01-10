# -*- coding: utf-8 -*-

class Node:
    def __init__(self, node_type):
        self.type = node_type
        self.node_problems = []

    @property
    def name(self):
        return ""

    @property
    def problems(self):
        return self.node_problems

class ValueNode(Node):
    def __init__(self, node_type, value):
        super().__init__(node_type)
        self.value = value 

class ParentNode(Node):
    def __init__(self, node_type):
        super().__init__(node_type)
        self.__children = []
        self.__children_map = {}

    @property
    def problems(self):
        pbs = self.node_problems.copy()
        for chld in self.__children:
            pbs.extend(chld.problems)
        return pbs

    def _get_children(self, name=None):
        if name is None:
            return self.__children
        else:
            return self.__children_map.get(name, [])

    def _add_child(self, child):
        self.__children.append(child)
        if child.name not in self.__children_map:
            self.__children_map[child.name] = [child]
        else:
            self.__children_map[child.name].append(child)
