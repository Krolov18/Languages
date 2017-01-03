# coding: utf-8

from abc import ABC, abstractmethod


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


def main():
    pass

if __name__ == '__main__':
    main()
