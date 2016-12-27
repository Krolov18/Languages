# coding: utf-8

import sqlite3
from Number import Number
from operator import add, mul, sub, lt, gt, eq, le, ge, not_, floordiv, mod
from collections import deque, Iterable, Iterator, Sequence


class NumberGenerator:
    """
        Classe composée d'outils permettant la transformation d'un entier dans sa prononciation dans une langue donnée.
        Cette classe peut faire eniter vers graphie mais graphie vers entier.
        Elle peut aussi renvoyer le ou les arbres de dérivations.
    """
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
        for i, j in enumerate(l):
            if isinstance(j, list) and len(l[i]) >= 2:
                l[i].insert(0, '(')
                l[i].append(')')
        return l

    @staticmethod
    def add_symbols(l: Iterable) -> str:
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
    def times(start: int, step: int) -> Iterator:
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
    def int2str(i: int, d: dict) -> str:
        """
        :param i: entier
        :param d: dictionnaire avec en clé des entiers, en valeur un tuple (graphie, phonologie)
        :return: liste de couples (graphie, phonologie)
        """
        return d.get(i)

    @staticmethod
    def convert_str2int(s: str, cursor: sqlite3.Cursor) -> list:
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
    def convert_int2str(i: int, parser: Number, d: dict) -> list:
        parsing = parser.parse(
                    NumberGenerator.add_symbols(
                        NumberGenerator.chain(
                            *NumberGenerator.add_parentheses(
                                NumberGenerator.add_multiples(
                                    NumberGenerator.chunk(
                                        NumberGenerator.int2list(
                                            i
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
        if parsing[1] is not None:
            return list(map(lambda x: NumberGenerator.int2str(x, d), NumberGenerator.delete0(parsing[1])))
        else:
            return [NumberGenerator.int2str(int(parsing[0]), d)]

    @staticmethod
    def delete0(l: Sequence):
        return filter(lambda x: x != 0, l)

    @staticmethod
    def chain(*iterables: Iterator):
        for t in iterables:
            if not isinstance(t, (list, tuple)):
                yield t
            else:
                for element in t:
                    yield element

    @staticmethod
    def chain_total(*iterables: Iterator):
        for iterable in iterables:
            if not isinstance(iterable, (list, tuple)):
                yield iterable
            else:
                NumberGenerator.chain_total(iterable)


def Basec(n, i):
    sigma = dict(zip(range(0, n), range(-n, 0)))
    tmp_i = list(map(int, list(str(i))))
    if not all(y in sigma for y in tmp_i):
        raise ValueError()
    powers = range(0, len(tmp_i))[::-1]
    return map(lambda x: (x[0], n, x[1]), zip(tmp_i, powers))


# class Base(object):
#     def __init__(self, base: int, power: int):
#         self.base = base
#         self.power = power
#         self.sigma = dict(zip(range(base), range(-base, 0)))
#         self.decomposition = None
#
#     def decompose(self, i, j=20):
#         sortie = list()
#         if i == 0:
#             return [(i, 1)]
#         quotient, rest = divmod(i, self.base**(j*self.power))
#         while not quotient:
#             j -= 1
#             quotient, rest = divmod(i, self.base**(j*self.power))
#         sortie.append((quotient, self.base**(j*self.power)))
#         for x in range(j)[::-1]:
#             quotient, rest = divmod(rest, self.base**(x*self.power))
#             sortie.append((quotient, self.base**(x*self.power)))
#         self.decomposition = sortie
#
#     def override(self, exceptions):
#         if self.decomposition == []:
#             return None
#         else:
#             quotients, base = exceptions
#             filter(lambda x: , self.decomposition)

def find_j(n, base, puissance, j=0):
    _ = floordiv(n, base**(puissance*j))
    while _:
        j +=1
        _ = floordiv(n, pow(base, mul(puissance, j)))
    return j


def baseN(n, bases, j=20):
    y = 0
    while (n < pow(*bases[y])):
        y += 1
    # print(y)
    (base, power) = bases[y]
    q = n // pow(base, mul(power, j))
    while not q:
        j -= 1
        q = n // pow(base, mul(power, j))
    # print(j)
    for e in divmod(n, pow(base, mul(power, j))):
        return baseN(e, bases=bases, j=20)

def base(n, base, power, j):
    l = []
    rest = n
    j = find_j(n, base, power, j)
    for x in reversed(range(j)):
        quotient, rest = divmod(rest, pow(base, mul(x, power)))
        l.append((quotient, pow(base, mul(x, power))))
    return l


def decompose(n, X, Y):
    xc=max(x for x in X if x <= n)
    yc=max(y for y in Y if y <= n//xc)

    if n == 0: return set()
    else: return {(xc, yc), None} | {None, decompose(n-mul(xc, yc), X, Y)}


def concat(a: dict, b: dict, s: str):
    """
        '_' = epsilon ou effecement
        '+' = cas pour l'addition
        '*' = cas pour la multiplication
        '/' = forme libre
        ';' = cas pour les ordinaux
        '?' = cas de la liaison
    :param a:
    :param b:
    :param s:
    :return:
    """
    if s not in {'_', '+', '*', '/', ';', '?'}:
        raise ValueError("Le paramètre 's' doit être un choix entre 'A', 'Z', 'O', 'F' ou 'L'")

    x = a.get(s, None)
    y = b.get(s, None)

    if any(None for x in (x, y)):
        return (a.get("*"), b.get("*"))
    elif x.endswith(s) and y.startswith(s):
        return a[:-1] + b[1:]
    elif y.endswith(s) and x.startswith(s):
        return b[:-1] + a[1:]
    elif not all(s in x for x in [a, b]):
        raise ValueError(
            "Le paramètre 's' doit être présent dans les deux membres 'a' et 'b' pour qu'il y ait concaténation."
        )
    else:
        return (a, b)


def multiplier(a: int, b: int, lexicon: dict):
    return lexicon.get(
        mul(
            a,
            b
        ),
        concat(
            lexicon.get(
                a
            ),
            lexicon.get(
                b
            ),
            "*"
        )
    ).get(
        '/',
        None
    )


def addtionner(a: tuple, b: tuple, lexique: dict, flag="Z"):
    pass


def f(u, G):
    for l in range(2, len(u)+1):
        for i in range(0, len(u)-l+1):
            for k in range(i, i+l-1):
                pass


def enumerate(sequence, start=0, ope=add):
    n = start
    for elem in sequence:
        yield n, elem
        n = ope(n, 1)


def g(n, base, power, j):
    l = list()
    def f(n, base, power, j):
        if n < pow(base, power):
            l.append(n)
        else:
            j = find_j(n, base, power)-1
            for qr in divmod(n, pow(base, mul(power, j))):
                f(qr, base, power, j-1)
    f(n, base, power, j)
    return l


def main1():
    import sqlite3
    import pickle

    c = NumberGenerator()

    base = pickle.load(open('exceptions.pickle', 'rb')).get('français')
    parser = Number(excpetions=base)

    reche = "SELECT integer, ortho, phon FROM Lexique WHERE isinteger = 1"

    with sqlite3.connect('Lexique.db') as conn:
        cursor = conn.cursor()

    intp = range(1, 9999)

    # base2 = {x: (y, z) for x, y, z in cursor.execute(reche).fetchall()} # pour avoir int: (graphie, phonologie)
    base2 = {x: y for x, y, z in cursor.execute(reche).fetchall()}  # pour avoir int: graphie

    for x in map(lambda x: c.convert_int2str(x, parser, base2), intp): print(x)


def main2():
    from itertools import product
    from functools import reduce

    n = 3995
    power = 1
    base = 5
    print(g(n, base, power, 0))
    # print(floordiv(7, 2))
    # print([floordiv(n, pow(base, mul(power, x))) for x in range(find_j(n, base, power))[::-1]])
    # Y = [10**i for i in range(10)]
    # print(X)
    # print(Y)
    b, p = (10, 3)
    n = 8765678764653453673453
    # print([pow(b, mul(p, x)) for x in range(1, 10)])
    v = ((x-1, x, x+1) for x in range(10))
    bpc = next(v, (None,)*3)
    # print(max(x if n<=x else n for x in range(10)))
    while bpc != (None,)*3:
        b, p, c = bpc
        bpc = next(v, (None,)*3)
        # print(b, p, c)
    # print(divmod(n, max([x for x in [pow(b, mul(p, x)) for x in range(10)] if x <= n])))

    x = deque([(10, 3), (10, 2), (10, 1), (20, 1), (10, 1)])
    # print(divmod(1234, 10**3))
    # print(base(18769876, 100, 1, 0))
    # print(find_j(123456789, 10, 3))
    # for i in range(1000):
    # trouduc = list(map(int, str(1000)))
    # base_power = [(20, 1)]
    # chaine = list(map(lambda x: add(*x), product(enumerate(trouduc, len(trouduc) - 1, sub), base_power)))
    # print(dict(zip(range(0, 1000), range(-1000, 0))))
    # qq = list(map(lambda x: mul(x[1], pow(x[2], mul(x[3], x[0]))), chaine))
    # print(reduce(lambda x, y: x + y, qq), qq, chaine)
    # print(int(x="1000", base=20))

    number = 18769876
    # print(base(number, 10, 3))
    # for basex in range(2, 12):
    #     print(str(basex)+":\t\t", " ".join(map(str, [x[0] for x in base(number, basex, 1)])))
    # print(" ".join(map(str, [x[0] for x in base(60, 60, 1)])), sep='\n')
    # print(2**(9*3)+5**(9*2)+1**(9*1)+4**(9*0))
    # print(map(str, list("817358231")))


if __name__ == '__main__':
    main2()

