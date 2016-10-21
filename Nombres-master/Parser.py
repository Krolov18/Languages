# coding: utf-8

import ply.lex as lex
import ply.yacc as yacc
import os
from NumberLexicon import NumberLexicon
import pickle


tokens = NumberLexicon.tokens


class Parser:
    """
        Classe inspirée de http://www.juanjoconti.com.ar/files/python/ply-examples/classcalc/calc.py

        Séparation de lex et de yacc afin de pouvoir utiliser l'un et l'autre indépendamment.
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.base = kw.get('excpetions', None)
        self.names = {}
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "_".join(["parser", self.__class__.__name__])
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"

        # Build the lexer and parser
        self.lexer = lex.lex(
            module=self,
            debug=self.debug
        )
        self.yacc = yacc.yacc(
            module=self,
            debug=self.debug,
            debugfile=self.debugfile,
            tabmodule=self.tabmodule
        )

    def run_while(self):
        while 1:
            try:
                s = input('translate > ')
            except EOFError:
                break
            if not s:
                continue
            print(self.yacc.parse(s))

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

    def parse(self, c: str) -> str:
        return yacc.parse(c)


def main():
    pass

if __name__ == '__main__':
    main()