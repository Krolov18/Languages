# coding: utf-8

import sqlite3
import typing
from Number import Number
from abc import ABC, abstractmethod


class NumberGenerator:
    @staticmethod
    def int2list(i: int) -> list:
        if i < 10:
            i = '0%d' % i
        return list(map(int, list(str(i))))

    @staticmethod
    def chunk(l: list, len_chunk=3) -> list:
        sortie = list()
        len_l = len(l)
        l_chunk = len_l % len_chunk
        if l_chunk != 0:
            rest = list()
            if l_chunk != 0:
                sortie.append(l[:l_chunk])
                rest = l[l_chunk:]
            sortie.extend([rest[len_chunk*x:len_chunk*(x+1)] for x in range(len(rest)//len_chunk) if rest != []])
            return sortie
        else:
            return [l[len_chunk*x:len_chunk*(x+1)] for x in range(len_l // len_chunk)]

    @staticmethod
    def add_multiples(l: list) -> list:
        from itertools import zip_longest

        if len(l) > 1:
            l = [x for x in list(
                NumberGenerator.chain(
                    *zip_longest(
                        l,
                        reversed(
                            NumberGenerator.get_multiples(
                                1000,
                                len(l)
                            )
                        )
                    )
                )
            ) if x is not None]
        for (k, j) in enumerate(l):
            if isinstance(j, list):
                l[k] = [x for x in list(
                    NumberGenerator.chain(
                        *zip_longest(
                            l[k],
                            reversed(
                                NumberGenerator.get_multiples(
                                    10,
                                    len(l[k])
                                )
                            )
                        )
                    )
                ) if x is not None]
        return l

    @staticmethod
    def add_parentheses(l: list):
        print(l)
        for i ,j in enumerate(l):
            if isinstance(j, list) and len(l[i]) >= 2:
                l[i].insert(0, '(')
                l[i].append(')')
        return l

    @staticmethod
    def add_symbols(l: list) -> str:
        import re

        tmp = list(map(str, l))
        for i, x in enumerate(tmp):
            if re.search(r'100*', x):
                tmp[i] = "*{0}+".format(x).split(' ')
        return "".join(list(NumberGenerator.chain(*tmp)))

    @staticmethod
    def get_multiples(n: int, i: int) -> list:
        gen = NumberGenerator.times(n, n)
        return [next(gen) for _ in range(1, i)]

    @staticmethod
    def times(start: int, step: int) -> typing.Iterator:
        n = start
        while True:
            yield n
            n *= step

    @staticmethod
    def str2int(s: str, cursor: sqlite3.Cursor) -> int:
        """
            On interroge une base données, on vérifie si la chaine de caractère est soit
            dans la case phonologie, soit dans la case graphie et on renvoie tous les entiers correspondants.
        :param s: chaine de caractères
        :param cursor: pointeur de base de données
        :return: l'entier associé à la chaine de caractères d'entrée, False sinon
        """
        recherche = "SELECT integer FROM Lexique WHERE ortho = ? OR phon = ?"
        cursor.execute(recherche, (s,)*2)
        return cursor.fetchone()

    @staticmethod
    def int2str(i: int, cursor: sqlite3.Cursor) -> str:
        """
            On interroge une base de données, on vérifie si l'entier fourni en paramètre
            se trouve dans la base, si oui, on renvoie tous les couples (graphie, phonlogie)
            pouvant correspondre à l'entier en question.
        :param i: entier
        :param cursor:
        :return: liste de couples (graphie, phonologie)
        """
        recherche = "SELECT ortho, phon FROM Lexique WHERE integer = ?"

        cursor.execute(recherche, [str(i)])
        return cursor.fetchall()

    @staticmethod
    def convert_str2int(s: str, cursor: sqlite3.Cursor) -> typing.List[str]:
        import re
        return map(
            lambda x: NumberGenerator.str2int(
                x,
                cursor
            ),
            re.findall(
                r'\w+',
                s
            )
        )

    @staticmethod
    def convert_int2str(i: int, parser: Number, cursor: sqlite3.Cursor) -> typing.List[int]:
        return map(
            lambda x: NumberGenerator.int2str(x, cursor),
            map(
                int,
                parser.parse(
                    NumberGenerator.add_symbols(
                        NumberGenerator.add_multiples(
                            NumberGenerator.chunk(
                                NumberGenerator.int2list(
                                    i
                                ),
                                3
                            )
                        )
                    )
                )
            )
        )

    @staticmethod
    def chain(*iterables: typing.Iterator):
        for t in iterables:
            if not isinstance(t, (list, tuple)):
                yield t
            else:
                for element in t:
                    yield element

    @staticmethod
    def chain_total(*iterables: typing.Iterator):
        for iterable in iterables:
            if not isinstance(iterable, (list, tuple)):
                yield iterable
            else:
                NumberGenerator.chain_total(iterable)


def main():
    import itertools
    import sqlite3
    tmp = Number()
    with sqlite3.connect('Lexique.db') as conn:
        cursor = conn.cursor()
    intp = 7102469827103726
    print(NumberGenerator.add_symbols(list(NumberGenerator.chain(*NumberGenerator.add_parentheses(NumberGenerator.add_multiples(NumberGenerator.chunk(NumberGenerator.int2list(intp))))))))

if __name__ == '__main__':
    main()
