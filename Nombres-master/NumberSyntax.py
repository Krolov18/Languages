# coding: utf-8

import Syntax


class NumberSyntax(Syntax.Syntaxe):
    @staticmethod
    def p_s_1(p):
        """
            S : T PLUS unit
        """
        pass

    @staticmethod
    def p_s_2(p):
        """
            S : T PLUS S
        """
        pass

    @staticmethod
    def p_s_3(p):
        """
            S : '(' S ')'
        """
        p[0] = p[2]

    @staticmethod
    def p_t_1(p):
        """
            T : S TIMES multi
        """
        pass

    @staticmethod
    def p_t_2(p):
        """
            T : unit TIMES multi
        """
        pass


def main():
    pass

if __name__ == '__main__':
    main()
