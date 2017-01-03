# coding: utf-8

import NumberSyntax10
import NumberSyntax20
import DocStringInheritance


class Base10Base20(NumberSyntax10.NumberSyntaxe10, NumberSyntax20.NumberSyntax20):

    @DocStringInheritance.DocInherit
    def p_t_1(self, p):
        Base10.Base10.p_t_1(self, p)

    @DocStringInheritance.DocInherit
    def p_t_1(self, p):
        pass
