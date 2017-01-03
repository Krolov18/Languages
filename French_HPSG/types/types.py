# coding: utf-8

class SubClassError(TypeError):
    def __init__(self, giventype, expectedtype):
        self.giventype = type
        self.expectedtype = type
        self.message = """
            {self.giventype} doit être un sous type de {self.expectedtype},
            ce qui n'est pas le cas...""".format(
            self=self
        )

class InstanceClassError(SubClassError):
    def __init__(self, giventype, expectedtype):
        super().__init__(giventype=giventype, expectedtype=expectedtype)
        self.message = """
            {self.giventype} doit être une instance de {self.expectedtype}""".format(
            self=self
        )



class sign(object):
    def __init__(self, phon, synsem):
        if issubclass(phon, phonology):
            self.PHON = phon
        else:
            raise SubClassError(type(phon), phonology)
        if issubclass(synsem, synsem)
            self.SYNSEM = synsem
        else:
            raise SubClassError(synsem, synsem)


class phrase(sign):
    def __init__(self, phon, synsem, daughters):
        super().__init__(phon, synsem)
        if issubclass(daughters, feature_structure):
            self.DTRS = daughters
        else:
            raise SubClassError(daughters, feature_structure)


class word(sign): pass


class lexeme(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


class name(parent(s)): pass


