# coding: utf8

from typing import *


class Sommet(object):
    def __init__(self, x):
        self._parent = x
        self._rang = 0

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        pass

    @property
    def rang(self):
        return self._rang

    @rang.setter
    def rang(self, value):
        pass

    def __repr__(self):
        return "<{self._parent}, {self._rang}>".format(self=self)

    def __str__(self):
        return repr(self)


class Variable(Sommet):
    def __init__(self, x):
        super().__init__(x)


class Atome(Sommet):
    def __init__(self, x):
        super().__init__(x)


class Graphe(object):
    def __init__(self, graphe):
        import collections
        import itertools

        self.sommets = dict(zip(set(itertools.chain(graphe.keys())), len(set(itertools.chain(graphe.keys())))*[set()]))
        self.aretes = collections.OrderedDict(sorted(graphe.items(), lambda x: x[2]))

    def kruskal(self, graphe):
        sortie = set()
        for a in graphe.aretes:
            if self.find(a.u) != self.find(a.v):
                sortie |= {a}
                self.union(a.u, a.v)
        return sortie

    def union(self, x, y):
        if not all(map(lambda z: isinstance(z, Sommet), (x, y))):
            raise TypeError('x et y doivent être tous les deux Sommet.')

        xracine = self.find(x)
        yracine = self.find(y)
        if xracine != yracine:
            if xracine.rang < yracine.rang:
                xracine.parent = yracine
            else:
                yracine.parent = xracine.parent
                if xracine.rang == yracine.rang:
                    xracine.rang += 1

    def find(self, x):
        if x.parent != x:
            x.parent = self.find(x.parent)
        return x.parent

    def unify(self, t1, t2):
        if not all(map(lambda x: isinstance(x, (Atome, list, Variable)), [t1, t2])):
            raise TypeError('')
        else:
            t1 = self.find(t1)
            t2 = self.find(t2)
            if t1 == t2:
                return True
            elif all(map(lambda x: isinstance(x, Variable), [t1, t2])):
                self.union(t1, t2)
                return True
            elif (
                    (
                        isinstance(t1, Variable) and isinstance(t2, Atome)
                    ) or (
                            isinstance(t1, Atome) and isinstance(t2, Variable)
                    )
            ):
                if self.apparaitDans(t1, t2):
                    return False
                else:
                    t2.parent = t1.parent
                    return True
            elif all(map(lambda x: isinstance(x, list), [t1, t2])):
                if t1 == t2:
                    self.union(t1, t2)
                    return self.unify(t1, t2)
                else:
                    return False

    def unify_Lists(self, L: list, M: list) -> bool:
        if ((L ==  []) and (M == [])):
            return True
        elif len(L) != len(M):
            return False
        LL = L.pop(0)
        MM = M.pop(0)
        if self.Unify(LL, MM):
            return self.Unify_Lists(L, M)
        else:
            return False

    def apparaitDans(self, x: Variable, t: Axiome) -> bool:
        temps = 0
        return self.ApparaitDansBis(x, t, temps)

    def apparaitDansBis(self, x: Variable, t: Atome, temps: int) -> bool:
        if isinstance(t, Variable):
            return x == t
        elif isinstance(t, list):
            if t.poincon == temps:
                return False
            else:
                t.poincon = temps
                return self.ApparaitDansBis(x, t)

    def apparaitDansListe(self, x: Variable, L: list, temps: int):
        if L == []:
            return False
        LL = L.pop(0)
        if self.ApparaitDansBis(x, Atome(self.Find(LL)), temps):
            return True
        else:
            return self.ApparaitDansListe(x, L)


# Graphe = NewType('Graphe', Graphe)
