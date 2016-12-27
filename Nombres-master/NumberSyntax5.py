# coding: utf-8

import NumberSyntax
from abc import abstractmethod
import DocStringInheritance


class NumberSyntax5(NumberSyntax.NumberSyntax):
    @DocStringInheritance.DocInherit
    def p_t(self, p):
        if p[3] != '5':
            return False
        return True


def main():
    c = NumberSyntax5()
    print(c)

if __name__ == '__main__':
    main()
