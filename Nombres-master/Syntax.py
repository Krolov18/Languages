# coding: utf-8

from abc import ABC


class Syntaxe(ABC):
    @staticmethod
    def p_error(p):
        print("Syntax error at '%s'" % p.value)
