# coding: utf-8

import NumberSyntax
import DocStringInheritance
import re


class NumberSyntaxe10(NumberSyntax.NumberSyntax):
    @DocStringInheritance.DocInherit
    def p_t_1(self, p):
        if not re.match(r'10+', p[3]):
            raise ValueError("'multi' doit impérativement être 10**n avec n supérieur ou égal à 1.")

    @DocStringInheritance.DocInherit
    def p_t_2(self, p):
        if not re.match(r'10+', p[3]):
            raise ValueError("'multi' doit impérativement être 10**n avec n supérieur ou égal à 1.")
