# coding: utf-8

from ply import yacc, lex
import collections
from Unification import *


class TdlLexicon(object):
    #liste des tokens
    tokens = (
                "CLASS",
                "FEATURE"
            )
    literals = ("[", "]", ".", ":", "=", "&", ",")

    t_ignore = ' \t\n'

    def t_CLASS(self, t):
        r"""[a-z][a-z_0-9]*"""
        return t

    def t_FEATURE(self, t):
        r"""[A-Z][A-Z0-9]+"""
        return t

    def t_newline(self, t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        import sys
        print("Caractère illégal '{0}'".format(t.value[0]))
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, optimize=1, lextab="TdlLexicon", **kwargs)

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


class TdlSyntax(collections.UserDict):
    """
        En hériant de UserDict, on peut ainsi ajouter chaque résultat de parsing à l'attribut d'instance 'data'.
    """
    def __init__(self, *args, **kwargs):
        import collections

        super().__init__(args, kwargs)

        self.peres = collections.defaultdict(
            lambda : collections.defaultdict(
                lambda : collections.defaultdict(
                    bool
                )
            )
        )

    def p_S_1(self, p):
        """
            S : CLASS ':=' parents '.'
        """
        if p[1] in peres:
            raise TypeError('Le type que vous voulez définir a déjà été défini.')
        else:
            unif = unify(p[3])
            if unif:
                for pere in p[2]:
                    self.peres[pere][p[1]]['h'] = True
                for trait in unif:
                    self.peres[p[1]][trait] = unif[trait]
        # si p[1] in types retourner une redéfinition prohibée
        # sinon si unify(p[3]) échoue retourner une erreur sinon: for x in p[2]: types[x][p[1]]['h'] = True
        # unify(p[3]);
        types[p[1]] = map(unify, p[3])
        self.peres[p[1]].add(p[3])

    def p_S_2(self, p):
        """
            S : CLASS ':=' parents tmp '.'
        """
        types[p[1]] = self.unify(map(self.unify, p[3]), p[4])


    def p_tmp(self, p):
        """
            tmp : '[' constraints ']'
        """

    def p_constraint_1(self, p):
        """
            constraint : FEATURE CLASS
        """

    def p_constraint_2(self, p):
        """
            constraint : FEATURE tmp
        """

    def p_constraints_1(self, p):
        """
            constraints : ',' constraint
        """

    def p_constraints_2(self, p):
        """
            constraints : constraints
        """

    def unify(self):
        pass


def unifier_dict(dico1:dict, dico2:dict) -> dict:
    tmp = set(dico1.keys()).intersection(set(dico2.keys()))
    if tmp == set():
        return dico1.update(dico2)
    elif tmp != set():



def main():
    test = TdlLexicon()
    test.build()
    test.test("class1 := parent1 & parent2 & [FEAT1 value1,FEAT2 value2].")

if __name__ == '__main__':
    main()
