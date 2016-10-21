# coding: utf-8

class Node(object):
    def __init__(self, **kwargs):
        self.pere = kwargs.get("pere", None)
        self.children = kwargs.get("children", list())

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "[ .{pere} {children} ]".format(pere=self.pere, children= " ".join(map(str, self.children)))