# coding: utf-8
from abc import ABC, abstractmethod
from DocStringInheritance import DocInherit
from functools import reduce
from operator import mul, add


class NumberSyntax(ABC):
    """
        Classe abstrtaite ne définissant que la syntaxe du langage algébrique.
        Chaque règle, soit chaque méthode devra être implémentée.

        Le but de cette structure est de définir précisément le comportement des nombres dans une langue donnée.

        PLY utilise les doctrings pour écrire les productions de la grammaire, du coup, toute classe implémentant
        cette classe devra ajouter le décorateur @DocInherit au dessus de chaque règle afin de récupérer la docstring
        correspondante.
    """
    @staticmethod
    def exception(key: int or str, language: str) -> int or str:
        import pickle

        return key in pickle.load(open('exceptions.pickle', 'rb')).get(language, KeyError)

    @abstractmethod
    def p_s(self, p):
        """
            S : T PLUS unit
              | T PLUS S
        """
        raise NotImplementedError("Can't instantiate abstract class NumberSyntax with abstract method : p_s")

    @abstractmethod
    def p_t(self, p):
        """
            T : S TIMES multi
              | unit TIMES multi
        """
        raise NotImplementedError("Can't instantiate abstract class NumberSyntax with abstract method : p_t")

    @abstractmethod
    def p_unit(self, p):
        """
            unit : UNIT
        """

    @abstractmethod
    def p_multi(self, p):
        """
            multi : MULTI
        """


class NumberSyntaxFrench(NumberSyntax):
    """
        Dans un premier temps cette classe est uniquement optimisée pour la langue françise.
        Dans l'avenir, le système de numération d'une langue ne sera pas définie dans une classe mais dans l'héritage
        de plusieurs classes
    """
    @DocInherit
    def p_s(self, p):
        tmp = reduce(add, [reduce(mul, p[1]), reduce(add, p[3])])
        solution = NumberSyntax.exception(tmp, 'french')
        if solution:
            p[0] = [tmp]
        else:
            p[0] = p[1] + p[3]

    @DocInherit
    def p_t(self, p):
        tmp = reduce(mul, [reduce(add, p[1]), p[3]])
        solution = NumberSyntax.exception(tmp, 'french')
        if solution:
            p[0] = [tmp]
        else:
            p[0] = p[1] + p[3]

    @DocInherit
    def p_unit(self, p):
        p[0] = [p[1]]

    @DocInherit
    def p_multi(self, p):
        p[0] = [p[1]]


def main():
    pass

if __name__ == '__main__':
    main()
