# coding: utf-8

from abc import ABC, abstractmethod
from DocStringInheritance import DocInherit
from functools import reduce
from operator import mul, add


class ETF(ABC):
    """
        Base class for any parsers needing to use additions and multiplications.
    """
    @abstractmethod
    def p_e_1(self, p):
        """ E : E '+' T """
        pass

    @abstractmethod
    def p_e_2(self, p):
        """ E : T """
        pass

    @abstractmethod
    def p_t_1(self, p):
        """ T : T '*' F """
        pass

    @abstractmethod
    def p_t_2(self, p):
        """ T : F """
        pass

    @abstractmethod
    def p_f_1(self, p):
        """ F : '(' E ')' """
        pass

    @abstractmethod
    def p_f_2(self, p):
        """ F : UNIT """
        pass

class R(ETF):
    @DocInherit
    def p_e_1(self, p):
        pass

    @DocInherit
    def p_e_2(self, p):
        pass

    @DocInherit
    def p_t_1(self, p):
        pass

    @DocInherit
    def p_t_2(self, p):
        pass

    @DocInherit
    def p_f_1(self, p):
        pass

    @DocInherit
    def p_f_2(self, p):
        pass


def main():
    x = R()

if __name__ == '__main__':
    main()