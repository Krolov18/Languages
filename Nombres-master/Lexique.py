# coding: utf-8


class Lexique():
    tokens = ()
    literals  =()

    @staticmethod
    def t_error(t):
        print("Syntax error at '%s'" % t.value)
