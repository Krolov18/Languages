# coding: utf8

from collections import defaultdict
from nltk.util import everygrams
from numpy import zeros, array


def variabilise(chaine, spa):
    """
        variabilise('iront', (1, 2))
            > ('i', Variable('ro'), 'nt')
    :param chaine: chaine de caratère représentant le type concret
    :type: string
    :param spa: tuple d'entiers représentant la portion de chaine à variabiliser
    :return: une liste avec un découpage
    """
    if len(spa) == 1:
        # print([x for x in [chaine[:spa[0]], Variable(chaine[spa[0]]), chaine[spa[0] + 1:]]])
        print([x for x in [chaine[:spa[0]], Variable(chaine[spa[0]]), chaine[spa[0] + 1:]]])
        return [x for x in [chaine[:spa[0]], Variable(chaine[spa[0]]), chaine[spa[0] + 1:]] if x != ""]
    else:
        return [x for x in [chaine[:spa[0]], Variable(chaine[spa[0]:spa[-1] + 1]), chaine[spa[-1] + 1:]] if x != ""]


def span(courant):
    return everygrams([x for x, y in enumerate(courant)])


def abstraire(courant, ancetre):
    """
        Cette fonction consiste à partir d'un objet ChaineConcrete pour aller vers une Chaine Abstraite
        toute en passant par des ChaineSAbstraite (mélange de nonterminaux et terminaux afin de produire
        une hiérarchie descendante héritante des variables.

        Ex: si ancetre = iront, et courant = Xront
                alors X vaudra 'i'
            Si ancetre = Xront et que courant = XrY
                alors X vaudra toujours i et Y vaudra alors 'ont'

        Cette fonction génère la totalité de l'arbre. Algorithme basé sur les ngrams, plus la chaine est longue plus
        l'execution sera longue.

    :param courant: Chaine courante
    :type: Chaine
    :param ancetre: Chaine qui produit la Chaine courante
    :type: Chaine
    :return: None
    """
    enum_courant = enumerate(courant)
    if isinstance(courant, ChaineAbstraite):
        Type(courant, ancetre)
        return
    else:
        if isinstance(courant, ChaineConcrete):
            Type(courant, courant)
            lignee = (variabilise(courant, spa) for spa in span(courant))
        else:
            Type(courant, ancetre)
            lignee = []
            for i, element in enum_courant:
                debut = courant[:i]
                fin = courant[i+1:]
                if not isinstance(element, Variable):
                    for spa in span(element):
                        temp = variabilise(element, spa)
                        if i == 0:
                            lignee.append(temp+fin)
                        elif i == len(courant):
                            lignee.append(debut+temp)
                        else:
                            lignee.append(debut+temp+fin)
    for descendant in lignee:
        abstraire(descendant, courant)


def abstraction(chaine, ancestor):
    if all(isinstance(x, Variable) for x in chaine):
        # print(Type(chaine, ancestor))
        # print()
        # print()
        return
    else:
        if isinstance(chaine, ChaineConcrete):
            # print(Type(chaine, chaine))
            # print()
            spans = everygrams([x for x, y in enumerate(chaine)])

            lignee = [variabilise(chaine, span) for span in list(spans)]
        else:
            # print(Type(chaine, ancestor))
            # print()
            lignee = []
            for i, element in enumerate(chaine):
                debut = [chaine[:i]]
                fin = [chaine[i+1:]]
                if not isinstance(element, Variable):
                    spans = everygrams([x for x, y in enumerate(element)])
                    for span in spans:
                        chainex = variabilise(element, span)
                        print(chainex, fin)
                        if i == 0:
                            lignee.append(chainex + fin)
                        elif i == len(chaine) - 1:
                            lignee.append(debut + chainex)
                        else:
                            lignee.append(debut + chainex + fin)
    for descendant in lignee:
        abstraction(descendant, chaine)


class Paradigme(object):
    __paradigmes = defaultdict(list)
    __peres = defaultdict(list)

    def __init__(self, chaine, ancestor):
        self.name = str(chaine)
        self.ancestor = ancestor
        self.variables = chaine.variables
        self.regex = chaine.regex

        if len(type(self).__paradigmes[self.name]) == 0:
            type(self).__paradigmes[self.name].extend(self.variables)
        else:
            for i in range(len(self.variables)):
                type(self).__paradigmes[self.name][i] |= self.variables[i]

        type(self).__peres[self.name].append(self.ancestor)

    @staticmethod
    def getparadigmes():
        return Paradigme.__paradigmes

    @staticmethod
    def getperes():
        return Paradigme.__peres

    def matrice(self):
        cles = list(type(self).__peres.keys())
        taille = len(list(cles))
        enum_peres = enumerate(cles)
        temp = zeros((taille, taille))
        for (i, ligne) in enum_peres:
            for (j, col) in enum_peres:
                if type(self).__peres[ligne] == col:
                    temp[i][j] = 1
        return temp


class ChaineConcrete(object):
    """
        Cette object permet de définir ce qu'on veut qu'il soit dit concret.
    """
    def __init__(self, obj):
        self.object = obj

    def __repr__(self):
        return self.object

    def __str__(self):
        return repr(self)

    def __iter__(self):
        for x in self.object:
            yield x

    def __getitem__(self, item):
        return self.object[item]


class ChaineAbstraite(object):
    def __init__(self, obj):
        self.object = obj

    def __repr__(self):
        return self.object

    def __str__(self):
        return repr(self)


class ChaineSAbstraite(object):
    def __init__(self, obj):
        self.object = obj

    def __repr__(self):
        return self.object

    def __str__(self):
        return repr(self)


class Variable(object):
    """
        Type permettant d'identifier une partie d'un paradigme.
    """
    _variables = defaultdict(set)

    def __init__(self, variable):
        """

        :param variable:
        :return:
        """
        self.__name = variable
        self.__level = ""

    @property
    def getname(self):
        """

        :return:
        """
        return self.__name

    @property
    def getlevel(self):
        return self.__level

    def __repr__(self):
        """
            V pour variable et le numéro pour le niveau d'abstraction soit le nombre de variable dans la séquence.
            "iront" niveau concret soit V:0
            "V:1V:2V:3V:4" niveau abstrait soit V:4
            "V:1ront" niveau semi-abstrait soit V:1
        :return:
        """
        return "{self.getname}".format(self=self)

    def __str__(self):
        """

        :return:
        """
        return repr(self)

    def __len__(self):
        """

        :return:
        """
        return 1

    def __eq__(self, other):
        if self.__name == other.getname:
            return True
        return False

    def __hash__(self):
        return 1


class Type(object):
    """

    """
    _subtypes = defaultdict(lambda : defaultdict(set))
    _nb = 0

    def __init__(self, chaine, ancestor):
        """
        :param chaine:
        :param ancestor:
        :return:
        """
        self.name = "".join([str(x) for x in chaine])
        self.chaine = chaine
        self.ancestor = ancestor
        for (i, var) in enumerate(start=1, iterable=[x for x in chaine if isinstance(x, Variable)]):
            type(self)._subtypes[str(self)][i].add(var)

    def __repr__(self):
        """
            La représentation d'un type est au format TDL soit le format de déclaration
            de type pour HPSG.

        :return: type := parent &
                 [ CONTRAINTES].
        :type: string
        """
        return "{self.name}".format(self=self)

    def __str__(self):
        """
            quand str(instance) de Type est lancée, c'est le résultat de cette fonction qui est retourné.

        :return: repr(self)
        :type: string
        """
        return repr(self)


class Chaine(object):
    """
        Classe générique permettant dans un premier temps de représenter une Chaine de caractères
    """
    def __init__(self, chaine):
        self.chaine = chaine

    def __repr__(self):
        return self.chaine

    def __str__(self):
        return repr(self)

if __name__ == '__main__':
    abstraire(ChaineConcrete('iront'), ChaineConcrete('iront'))
    print(Type._subtypes)
    # abstraction('iront', 'iront')
