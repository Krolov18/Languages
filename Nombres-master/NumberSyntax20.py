# coding: utf-8

import DocStringInheritance
import re
import NumberSyntax


class NumberSyntax20(NumberSyntax.NumberSyntax):
    @DocStringInheritance.DocInherit
    def p_t_1(self, p):
        if not re.match(r'20', p[3]):
            raise ValueError("'multi' doit impérativement être 20.")


    @DocStringInheritance.DocInherit
    def p_t_2(self, p):
        if not re.match(r'20', p[3]):
            raise ValueError("'multi' doit impérativement être 20.")
