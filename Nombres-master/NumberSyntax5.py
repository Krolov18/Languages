# coding: utf-8

import NumberSyntax
from abc import abstractmethod
import DocStringInheritance


class NumberSyntax5(NumberSyntax.NumberSyntax):
    @DocStringInheritance.DocInherit
    def p_t_1(self, p):
        if p[3] != '5':
            raise ValueError("'multi' doit impérativement être 5.")

    @DocStringInheritance.DocInherit
    def p_t_2(self, p):
        if p[3] != '5':
            raise ValueError("'multi' doit impérativement être 5.")
