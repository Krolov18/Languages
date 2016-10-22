# coding: utf-8

from abc import ABC


class Lexicon(ABC):
    tokens = ()
    literals  =()

    @staticmethod
    def t_error(t):
        print("Syntax error at '%s'" % t.value)
