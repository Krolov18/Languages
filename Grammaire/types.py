# coding: utf-8
import collections


class data(object):
    def __init__(self):
        pass


class string(object):
    def __init__(self, string):
        if issubclass(string, str):
            self._STR = string


class terminal(data):
    def __init__(self, chaine):
        super().__init__()
        if issubclass(chaine, chaine):
            self._CHA = chaine

    @property
    def CHA(self):
        return self._CHA


class chaine(string):
    def __init__(self, cha):
        super().__init__(cha)
        if cha.islower():
            self._STR = cha


class variable(string):
    def __init__(self, var):
        super().__init__(var)
        if var.isupper():
            self._STR = var


class nonterminal(data):
    def __init__(self, var, ref):
        super().__init__()
        if issubclass(var, variable):
            self._VAR = var
        else:
            raise TypeError('var {0} doit être un sous type de {1}'.format(type(var), variable))
        if issubclass(ref, chaine):
            self._REF = ref
        else:
            raise TypeError('ref {0} doit être un sous type de {1}'.format(type(ref), chaine))

    @property
    def VAR(self):
        return self._VAR

    @property
    def CHA(self):
        return self._REF


class axiome(nonterminal):
    def __init__(self, var, ref):
        super().__init__(var, ref)


class liste(object):
    def __init__(self, first):
        if issubclass(first, object):
            self._FIRST = first
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(first), object))

    @property
    def FIRST(self):
        return self._FIRST


class liste_nonempty(liste):
    def __init__(self, first, rest):
        super().__init__(first)
        if issubclass(rest, liste):
            self._REST = rest
        else:
            raise TypeError('rest {0} doit être un sous type de {1}'.format(type(rest), liste))

    @property
    def REST(self):
        return self._REST


class terminals(liste_nonempty):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, terminal):
            self._FIRST = first


class terminals_empty(terminals):
    def __init__(self, first=None):
        super().__init__(first)
        if issubclass():
            self._FIRST = first
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(first), None))


class nonterminals(liste_nonempty):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, nonterminal):
            self._FIRST = first
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(first), nonterminal))


class nonterminals_empty(nonterminals):
    def __init__(self, first=None):
        super().__init__(first)
        if issubclass(first, None):
            self._FIRST = first
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(first), None))


class axiomes(liste_nonempty):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, axiome):
            self._FIRST = first
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(first), axiome))


class axiomes_empty(axiomes):
    def __init__(self, first):
        super().__init__(first)
        if issubclass(first, None):
            self._FIRST = first
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(first), None))


class productions(liste_nonempty):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, production):
            self._FIRST = first
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(first), production))


class productions_empty(productions):
    def __init__(self, first):
        super().__init__(first)
        if issubclass(first, None):
            self._FIRST = first
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(first), None))


class productions_unaires_binaires(productions):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, production_horscontexte_nonempty_binaire) or issubclass(first, production_horscontexte_nonempty_unaire):
            self._FIRST = first
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(first), " ou ".join([production_horscontexte_nonempty_unaire, production_horscontexte_nonempty_binaire])))


class productions_unaires_t_binaires_nt_nt(productions_unaires_binaires):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, production_horscontexte_nonempty_binaire_nt_nt) or issubclass(first, production_horscontexte_nonempty_unaire_t):
            self._FIRST = first
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(first), " ou ".join([production_horscontexte_nonempty_unaire, production_horscontexte_nonempty_binaire])))


class productions_horscontextes(productions):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, production_horscontexte):
            self._FIRST = first
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(first), production_horscontexte))


class grammaire():
    def __init__(self, terms, nonterms, axioms, prods):
        if issubclass(terms, terminals):
            self._TERMS = terms
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(terms), terminals))
        if issubclass(nonterms, nonterminals):
            self._NONTERMS = nonterms
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(nonterms), nonterminals))
        if issubclass(axioms, axiomes):
            self._AXIOMS = axioms
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(axioms), axiomes))
        if issubclass(prods, productions):
            self._PRODS = prods
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(prods), productions))

    @property
    def TERMS(self):
        return self._TERMS

    @property
    def NONTERMS(self):
        return self._NONTERMS

    @property
    def AXIOMS(self):
        return self._AXIOMS

    @property
    def PRODS(self):
        return self._PRODS


class grammaire_horscontexte(grammaire):
    def __init__(self, terms, nonterms, axioms, prods):
        super().__init__(terms, nonterms, axioms, prods)
        if issubclass(prods, productions_horscontextes):
            self._PRODS = prods


class grammaire_horscontexte_probabilisee(grammaire_horscontexte):
    def __init__(self, terms, nonterms, axioms, prods):
        super().__init__(terms, nonterms, axioms, prods)


class grammaire_horscontexte__chomskynormalform(grammaire_horscontexte):
    def __init__(self, terms, nonterms, axioms, prods):
        super().__init__(terms, nonterms, axioms, prods)
        if issubclass(productions_unaires_t_binaires_nt_nt):
            self._PRODS = prods


class grammaire_horscontexte_chomskynormalform_probabilisee(grammaire_horscontexte__chomskynormalform):
    def __init__(self, terms, nonterms, axioms, prods):
        super().__init__(terms, nonterms, axioms, prods)


class liste_empty(liste):
    def __init__(self, first):
        super().__init__(first)
        if issubclass(first, None):
            self._FIRST = first


class liste_nonempty_1(liste_nonempty):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, liste_empty):
            self._REST = rest

    @property
    def REST(self):
        return self._REST


class liste_nonempty_sup1(liste_nonempty):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, liste_nonempty):
            self._REST = rest

    @property
    def REST(self):
        return self._REST


class liste_nonempty_2(liste_nonempty_sup1):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, liste_nonempty_1):
            self._REST = rest

    @property
    def REST(self):
        return self._REST


class liste_nonempty_sup2(liste_nonempty_sup1):
    def __init__(self, first, rest):
        super().__init__(first, rest)


class liste_nonempty_3(liste_nonempty_sup2):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, liste_nonempty_2):
            self._REST = rest

    @property
    def REST(self):
        return self._REST


class liste_nonempty_sup3(liste_nonempty_sup2):
    def __init__(self, first, rest):
        super().__init__(first, rest)


class handside(liste):
    def __init__(self):
        super().__init__()


class handside_empty(liste_empty):
    def __init__(self):
        super().__init__()


class handside_nonempty(liste_nonempty):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, data):
            self._FIRST = first
        else:
            raise TypeError('first {0} doit être un sous type de {1}'.format(type(first), data))


class handside_nonempty_1(liste_nonempty_1):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_empty):
            self._REST = rest


class handside_nonempty_1_t(handside_nonempty_1):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, terminal):
            self._FIRST = first


class handside_nonempty_1_nt(handside_nonempty_1):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, nonterminal):
            self._FIRST = first


class handside_nonempty_sup1(liste_nonempty_sup1):
    def __init__(self, first, rest):
        super().__init__(first, rest)


class handside_nonempty_2(liste_nonempty_2):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_1):
            self._REST = rest


class handside_nonempty_2_t(handside_nonempty_2):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, terminal):
            self._FIRST = first


class handside_nonempty_2_t_t(handside_nonempty_2_t):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_1_t):
            self._REST = rest


class handside_nonempty_2_t_nt(handside_nonempty_2_t):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_1_nt):
            self._REST = rest


class handside_nonempty_2_nt(handside_nonempty_2):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, nonterminal):
            self._FIRST = first


class handside_nonempty_2_nt_t(handside_nonempty_2_nt):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_1_t):
            self._REST = rest


class handside_nonempty_2_nt_nt(handside_nonempty_2_nt):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_1_nt):
            self._REST = rest


class handside_nonempty_sup2(liste_nonempty_sup2):
    def __init__(self, first, rest):
        super().__init__(first, rest)


class handside_nonempty_sup3(liste_nonempty_sup3):
    def __init__(self, first, rest):
        super().__init__(first, rest)


class handside_nonempty_3(liste_nonempty_3):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_2):
            self._REST = rest


class handside_nonempty_3_t(handside_nonempty_3):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, terminal):
            self._FIRST = first


class handside_nonempty_3_t_t(handside_nonempty_3_t):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_2_t):
            self._REST = rest


class handside_nonempty_3_t_t_t(handside_nonempty_3_t_t):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_2_t_t):
            self._REST = rest


class handside_nonempty_3_t_t_nt(handside_nonempty_3_t_t):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_2_t_nt):
            self._REST = rest


class handside_nonempty_3_t_nt(handside_nonempty_3_t):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_2_nt):
            self._REST = rest


class handside_nonempty_3_t_nt_t(handside_nonempty_3_t_nt):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_2_nt_t):
            self._REST = rest


class handside_nonempty_3_t_nt_nt(handside_nonempty_3_t_nt):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_2_nt_nt):
            self._REST = rest


class handside_nonempty_3_nt(handside_nonempty_3):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(first, nonterminal):
            self._FIRST = first


class handside_nonempty_3_nt_t(handside_nonempty_3_nt):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_2_t):
            self._REST = rest


class handside_nonempty_3_nt_t_t(handside_nonempty_3_nt_t):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_2_t_t):
            self._REST = rest


class handside_nonempty_3_nt_t_nt(handside_nonempty_3_nt_t):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_2_t_nt):
            self._REST = rest


class handside_nonempty_3_nt_nt(handside_nonempty_3_nt):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_2_nt):
            self._REST = rest


class handside_nonempty_3_nt_nt_t(handside_nonempty_3_nt_nt):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_2_nt_t):
            self._REST = rest


class handside_nonempty_3_nt_nt_nt(handside_nonempty_3_nt_nt):
    def __init__(self, first, rest):
        super().__init__(first, rest)
        if issubclass(rest, handside_nonempty_2_nt_nt):
            self._REST = rest


class lefthandside(object):
    def __init__(self, lhs):
        super().__init__()
        if issubclass(lhs, handside_nonempty):
            self._LHS = lhs


class lefthandside_horscontexte(lefthandside):
    def __init__(self, lhs):
        super().__init__(lhs)
        if issubclass(lhs, handside_nonempty_1_nt):
            self._LHS = lhs


class righthandside(object):
    def __init__(self, rhs):
        super().__init__()
        if issubclass(rhs, handside):
            self._RHS = rhs

    @property
    def RHS(self):
        return self._RHS


class righthandside_empty(righthandside):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_empty):
            self._RHS = rhs


class righthandside_nonempty(righthandside):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_nonempty):
            self._RHS = rhs


class righthandside_nonempty_unaire(righthandside_nonempty):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_nonempty_1):
            self._RHS = rhs


class righthandside_nonempty_unaire_t(righthandside_nonempty_unaire):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_nonempty_1_t):
            self._RHS = rhs


class righthandside_nonempty_unaire_nt(righthandside_nonempty_unaire):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_nonempty_1_nt):
            self._RHS = rhs


class righthandside_nonempty_supunaire(righthandside_nonempty):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_nonempty_sup1):
            self._RHS = rhs


class righthandside_nonempty_binaire(righthandside_nonempty_supunaire):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_nonempty_2):
            self._RHS = rhs


class righthandside_nonempty_binaire_nt(righthandside_nonempty_binaire):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_nonempty_2_nt):
            self._RHS = rhs


class righthandside_nonempty_binaire_nt_t(righthandside_nonempty_binaire_nt):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_nonempty_2_nt_t):
            self._RHS = rhs


class righthandside_nonempty_binaire_nt_nt(righthandside_nonempty_binaire_nt):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_nonempty_2_nt_nt):
            self._RHS = rhs


class righthandside_nonempty_binaire_t(righthandside_nonempty_binaire):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_nonempty_2_t):
            self._RHS = rhs


class righthandside_nonempty_binaire_t_nt(righthandside_nonempty_binaire_t):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_nonempty_2_t_nt):
            self._RHS = rhs


class righthandside_nonempty_binaire_t_t(righthandside_nonempty_binaire_t):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_nonempty_2_t_t):
            self._RHS = rhs


class righthandside_nonempty_supbinaire(righthandside_nonempty_supunaire):
    def __init__(self, rhs):
        super().__init__(rhs)
        if issubclass(rhs, handside_nonempty_sup2):
            self._RHS = rhs


class production(object):
    def __init__(self, lhs, rhs):
        super().__init__()
        if issubclass(lhs, lefthandside):
            self._LHS = lhs
        else:
            raise TypeError('lhs {0} doit être un sous type de {1}'.format(type(lhs), lefthandside))
        if issubclass(rhs, righthandside):
            self._RHS = rhs
        else:
            raise TypeError('rhs {0} doit être un sous type de {1}'.format(type(rhs), righthandside))

    @property
    def LHS(self):
        return self._LHS

    @property
    def RHS(self):
        return self._RHS


class production_horscontexte(production):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(lhs, lefthandside_horscontexte):
            self._LHS = lhs


class production_horscontexte_empty(production_horscontexte):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_empty):
            self._RHS = rhs


class production_horscontexte_nonempty(production_horscontexte):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_nonempty):
            self._RHS = rhs


class production_horscontexte_nonempty_unaire(production_horscontexte_nonempty):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_nonempty_unaire):
            self._RHS = rhs


class production_horscontexte_nonempty_unaire_nt(production_horscontexte_nonempty_unaire):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_nonempty_unaire_nt):
            self._RHS = rhs


class production_horscontexte_nonempty_unaire_t(production_horscontexte_nonempty_unaire):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_nonempty_unaire_t):
            self._RHS = rhs


class production_horscontexte_nonempty_sup1(production_horscontexte_nonempty):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_nonempty_supunaire):
            self._RHS = rhs


class production_horscontexte_nonempty_binaire(production_horscontexte_nonempty_sup1):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_nonempty_binaire):
            self._RHS = rhs


class production_horscontexte_nonempty_binaire_t(production_horscontexte_nonempty_binaire):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_nonempty_binaire_t):
            self._RHS = rhs


class production_horscontexte_nonempty_binaire_t_t(production_horscontexte_nonempty_binaire_t):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_nonempty_binaire_t_t):
            self._RHS = rhs


class production_horscontexte_nonempty_binaire_t_nt(production_horscontexte_nonempty_binaire_t_t):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_nonempty_binaire_t_nt):
            self._RHS = rhs


class production_horscontexte_nonempty_binaire_nt(production_horscontexte_nonempty_binaire):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_nonempty_binaire_nt):
            self._RHS = rhs


class production_horscontexte_nonempty_binaire_nt_t(production_horscontexte_nonempty_binaire_nt):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_nonempty_binaire_nt_t):
            self._RHS = rhs


class production_horscontexte_nonempty_binaire_nt_nt(production_horscontexte_nonempty_binaire_nt):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_nonempty_binaire_nt_nt):
            self._RHS = rhs


class production_horscontexte_nonempty_sup2(production_horscontexte_nonempty_sup1):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        if issubclass(rhs, righthandside_nonempty_supbinaire):
            self._RHS = rhs


class production_contextuelle(production):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)


