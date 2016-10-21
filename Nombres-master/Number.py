# coding: utf-8

from Parser import Parser
from operator import mul, add
import typing


# class Number(Parser):
#     tokens = (
#         "UNIT",
#         "PLUS",
#         "TIMES",
#         "ZERO"
#     )
#
#     literals = ('(', ')', '+', '*')
#
#     # t_PLUS = r'\+'
#     # t_TIMES = r'\*'
#
#     @staticmethod
#     def t_UNIT(t):
#         r'\d+'
#         return t
#
#     @staticmethod
#     def t_ZERO(t):
#         r"""0"""
#         return t
#
#     @staticmethod
#     def t_newline(t):
#         r"""\n+"""
#         t.lexer.lineo += len(t.value)
#
#     t_ignore = ' \t'
#
#     @staticmethod
#     def t_error(t):
#         print('Je ne peux pas reconnaitre {0}'.format(t.value[0]))
#         t.lexer.skip(1)
#
#     def p_e_1(self, p):
#         """ E : E '+' T """
#         p[0] = [p[1], p[3]]
#
#     def p_e_2(self, p):
#         """ E : T """
#         p[0] = p[1]
#
#     def p_t_1(self, p):
#         """ T : T '*' F """
#         p[0] = [p[1], p[3]]
#
#     def p_t_2(self, p):
#         """ T : F """
#         p[0] = p[1]
#
#     def p_f_1(self, p):
#         """ F : '(' E ')' """
#         p[0] = p[2]
#
#     def p_f_2(self, p):
#         """ F : UNIT """
#         p[0] = p[1]
#
#     @staticmethod
#     def p_error(p):
#         print("Syntax error at '%s'" % p.value)

class Numbere(Lexique.Lexique):
    tokens = ("NUMBER", "PLUS", "TIMES")

    literals = ('(', ')')

    t_PLUS = r'\+'
    t_TIMES = r'\*'
    t_NUMBER = r'\d+'
    t_ignore = r'\t\n '



class Number(Parser):
    tokens = (
        "UNIT",
        "PLUS",
        "TIMES",
        "ZERO"
    )

    literals = ('(', ')')

    t_PLUS = r'\+'
    t_TIMES = r'\*'

    @staticmethod
    def t_UNIT(t):
        r"""(1|2|3|4|5|6|7|8|9)"""
        return t

    @staticmethod
    def t_ZERO(t):
        r"""0"""
        return t

    t_ignore = ' \t\n'

    @staticmethod
    def t_error(t):
        print('Je ne peux pas reconnaitre {0}'.format(t.value[0]))
        t.lexer.skip(1)

    def p_s_1(self, p):
        """
            S : T PLUS unit
        """
        p[0] = reduire(p[1], int(p[3]), add, self.base)

    def p_s_2(self, p):
        """
            S : T PLUS S
        """
        p[0] = reduire(p[1], p[3], add, self.base)

    @staticmethod
    def p_s_3(p):
        """
            S : '(' S ')'
        """
        p[0] = p[2]

    def p_t_1(self, p):
        """
            T : S TIMES multi
        """
        p[0] = reduire(p[1], int(p[3]), mul, self.base)

    def p_t_2(self, p):
        """
            T : unit TIMES multi
        """
        p[0] = reduire(int(p[1]), p[3], mul, self.base)

    @staticmethod
    def p_unit(p):
        """
            unit : UNIT
                 | ZERO
        """
        p[0] = p[1]

    @staticmethod
    def p_multi(p):
        """
            multi : UNIT zeros
        """
        p[0] = int("".join(p[1:]))

    @staticmethod
    def p_zeros(p):
        """
            zeros : ZERO
                  | ZERO zeros
        """
        import itertools
        if len(p) > 2:
            p[0] = "".join(list(itertools.chain(*[p[1]] + [p[2]])))
        else:
            p[0] = "".join(list(itertools.chain(*[p[1]])))

    @staticmethod
    def p_error(p):
        print("Syntax error at '%s'" % p.value)


def reduire(obj1: typing.Union[int, tuple, None], obj2: typing.Union[int, tuple, None], ope, base: dict) -> tuple:
    """
        Fonction qui permet de prendre deux objets, d'appliquer une fonctions sur eux et de retourner le résultat.
    :param obj1: entier pouvant être le résultat d'un calcul
                 un tuple représentant un calcul et (sa décomposition ou None si non décomposable)
    :param obj2: entier pouvant être le résultat d'un calcul
                 un tuple représentant un calcul et (sa décomposition ou None si non décomposable)
    :param ope: une fonction qui permet des opérations uniquement sur des entiers
    :param base: un dictionnaire représentant les formes non prédictibles ou non décomposables d'une langue
    :return: on retourne un tuple composé d'un entier et (d'un tuple d'entiers ou de None)
    """
    if isinstance(obj1, int) and isinstance(obj2, int):
        calcul = ope(obj1, obj2)
        if calcul in base:
            return calcul, None
        else:
            return calcul, (obj1, obj2)
    elif isinstance(obj1, tuple) and isinstance(obj2, int):
        calcul = ope(obj1[0], obj2)
        if calcul in base:
            return calcul, None
        else:
            if obj1[1] is None:
                return calcul, (obj1[0], obj2)
            else:
                return calcul, (obj1[1] + (obj2,))
    elif isinstance(obj1, tuple) and isinstance(obj2, tuple):
        calcul = ope(obj1[0], obj2[0])
        if calcul in base:
            return calcul, None
        else:
            if obj1[1] is None and obj2[1] is None:
                return calcul, (obj1[0], obj2[0])
            elif obj1[1] is None:
                return calcul, ((obj1[0],) + obj2[1])
            elif obj2[1] is None:
                return calcul, (obj1[1] + (obj2[0],))
            elif isinstance(obj1[1], tuple) and isinstance(obj2[1], tuple):
                return calcul, (obj1[1] + obj2[1])
    else:
        raise LookupError('Cas de figure non pris en compte')


def main():
    import pickle

    base = pickle.load(open('exceptions.pickle', 'rb')).get('français')
    tmp = Number(excpetions=base)
    c = tmp.parse(
        """ 7
            *
            1000000000000000
            +
            (1*100+0*10+2)
            *
            1000000000000
            +
            (4*100+6*10+9)
            *
            1000000000
            +
            (8*100+2*10+7)
            *
            1000000
            +
            (1*100+0*10+3)
            *
            1000
            +
            (7*100+2*10+6)
        """
    )
    d = tmp.parse("3*10000000000000+0")

    if d[1] is None:
        print(d[0])
    else:
        print(d[1])

if __name__ == '__main__':
    main()
