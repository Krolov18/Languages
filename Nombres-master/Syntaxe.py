# coding: utf-8

class Syntaxe():
    @staticmethod
    def p_error(p):
        print("Syntax error at '%s'" % p.value)
