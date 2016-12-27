# coding: utf-8

import Syntax
import DocStringInheritance



class NumberSyntax5(Syntax.Syntax):
    def p_s5_1(self, p):
        """
            S5 : T5 '+' UNIT4
        """

    def p_s5_2(self, p):
        """
            S5 : T5 '+' S5
        """

    def p_s5_3(self, p):
        """
            S5 : '(' S5 ')'
        """

    def p_t5_1(self, p):
        """
            T5 : S5 '*' MULTI5
        """

    def p_t5_2(self, p):
        """
            T5 : UNIT3 '*' MULTI5
        """


class NumberSyntax10(Syntax.Syntax):
    def p_s10_1(self, p):
        """
            S10 : T10 '+' UNIT10
        """

    def p_s10_2(self, p):
        """
            S10 : T10 '+' S10
        """

    def p_s10_3(self, p):
        """
            S10 : '(' S10 ')'
        """

    def p_t10_1(self, p):
        """
            T10 : S10 '*' MULTI10
        """

    def p_t10_2(self, p):
        """
            T10 : UNIT10 '*' MULTI10
        """

    @staticmethod
    def p_unit(p):
        """
            unit : UNIT
                 | ZERO
        """

    @staticmethod
    def p_multi(p):
        """
            multi : UNIT zeros
        """

    @staticmethod
    def p_zeros(p):
        """
            zeros : ZERO
                  | ZERO zeros
        """


class NumberSyntax20(Syntax.Syntax):
    def p_s20_1(self, p):
        """
            S20 : T20 '+' UNIT20
        """

    def p_s20_2(self, p):
        """
            S20 : T20 '+' S20
        """

    def p_s20_3(self, p):
        """
            S20 : '(' S20 ')'
        """

    def p_t20_1(self, p):
        """
            T20 : S20 '*' MULTI20
        """

    def p_t20_2(self, p):
        """
            T20 : UNIT20 '*' MULTI20
        """


class NumberSyntax5NumberSyntax20(NumberSyntax5, NumberSyntax20):
    def p_s20_1(self, p):
        """
            S20 : T20 '+' S5
        """

    def p_t20_2(self, p):
        """
            T20 : S5 '*' MULTI20
        """


class NumberSyntax10NumberSyntax20(NumberSyntax10, NumberSyntax20):
    x = 80 == 8*10 == [4, 2], '*', 10, '+'


def main():
    pass

if __name__ == '__main__':
    main()
