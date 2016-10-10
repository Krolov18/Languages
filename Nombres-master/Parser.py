# coding: utf-8

import ply.lex as lex
import ply.yacc as yacc
import os
from NumberLexicon import NumberLexicon


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
        self.names = {}
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "_".join(["parser", self.__class__.__name__])
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"

        # Build the lexer and parser
        lex.lex(
            module=self,
            debug=self.debug
        )
        yacc.yacc(
            module=self,
            debug=self.debug,
            debugfile=self.debugfile,
            tabmodule=self.tabmodule
        )

    @staticmethod
    def exception(key: int, language: str) -> dict:
        """
            Fonction permettant d'accéder aux formes non-décomposables.
            Pour l'instant celles-ci sont classées par langues.
        :param key: clé correspondant à un chiffre dans le dictionnaire
        :param language: chaine de caractère caractérisant la langue dans laquelle la clé doit être cherchée.
        :return: on retourne la vlaeur associée à la clé soit un dictionnaire à deux entrées ('graphie', 'phonologie')
        """
        import pickle
        return pickle.load(open('exceptions.pickle', 'rb')).get(language).get(key, False)

    @staticmethod
    def run_while():
        while 1:
            try:
                s = input('translate > ')
            except EOFError:
                break
            if not s:
                continue
            print(yacc.parse(s))

    def parse(self, c: str) -> str:
        return yacc.parse(c)


def main():
    pass

if __name__ == '__main__':
    main()