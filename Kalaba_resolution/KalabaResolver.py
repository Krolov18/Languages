__author__ = 'korantin'

from nltk.util import everygrams
from difflib import *
from traitementKalaba import FormeurTXT
from itertools import combinations,groupby
from codecs import open

class KalabaResolver:
    """
        Classe qui prend un corpus aligné en input. soit des couple (langue1,langue2) avec aucune annotation.
        Le but sera de donner une structure aux données. Nous sommes quand même dans un cadre:
        langue2|langue1 soit nous connaissons la langue1 et nous cherchons à connaitre des choses sur la langue2.
        A terme il se peut qu'une structure (langue1,langue2) soit insuffisante et alors on passera à
        (structure(langue1), langue2), le but restant le même, structurer langue2 à partir des connaissances de langue1.

        dans cette première version on par du principe que langue1 est découpable sur les " ".

        F = ensemble des phrases d'une langue
        K = ensemble des phrases d'une langue
        m = longueur d'une phrase f appartenant à F
        n = longueur d'une phrase k appartenant à K
        i = mot de f
        j = mot de k
        LF = lexique de F
        LK = lexique de K

    """
    def __init__(self,corpus):
        self.corpus = corpus
        self.corpusLangue1 = [x[0] for x in corpus]
        self.corpusLangue2 = [x[1] for x in corpus]
        self.lexiqueLangue1 = set()
        self.lexiqueLangue2 = set()
        self.remplirLexique()
        self.correspondancesLangue1 = {lexie:[] for lexie in self.lexiqueLangue1}
        self.correspondancesLangue2 = {lexie:[] for lexie in self.lexiqueLangue2}
        self.initialiseCorrespondances()

    def remplirLexique(self):
        for phrase in self.corpusLangue1:
            self.lexiqueLangue1 |= set([" ".join(x) for x in everygrams(phrase.split(' '))])
        for phras in self.corpusLangue2:
            self.lexiqueLangue2 |= set(["".join(x) for x in everygrams(list(phras))])

    def initialiseCorrespondances(self):
        for couple in self.corpus:
            (langue1,langue2) = couple
            for correspond1 in self.correspondancesLangue1:
                if correspond1 in [" ".join(x) for x in everygrams(langue1.split(' '))]:
                    if couple not in self.correspondancesLangue1[correspond1]:
                        self.correspondancesLangue1[correspond1].append(couple)
            for correspond2 in self.correspondancesLangue2:
                if correspond2 in langue2:
                    if couple not in self.correspondancesLangue2[correspond2]:
                        self.correspondancesLangue2[correspond2].append(couple)
def lePlusGrand(data,key=None,keyfunc=None):
    if key == None:
        key = lambda x: x
    elif keyfunc == None:
        keyfunc = lambda x: x
    groups = []
    uniquekeys = []
    data = sorted(data, key=key)
    for k, g in groupby(data, keyfunc):
        groups.append(list(g))      # Store group iterator as a list
        uniquekeys.append(k)
    return groups

def main():
    from sys import argv
    from codecs import open
    from itertools import islice

    corpus = [x.strip() for x in open(argv[1],"r","utf-8").readlines() if x != ""]
    francais = [phrase for phrase in islice(corpus,0,len(corpus),2)]
    kalaba = [phrase for phrase in islice(corpus,1,len(corpus),2)]
    corpus = list(zip(francais,kalaba))

    temp = KalabaResolver(corpus)
    dd = []
    deuxChasseurs = list(combinations(temp.correspondancesLangue1["deux chasseurs"],2))[0]
    # print(deuxChasseurs)
    # desChasseurs = list(combinations(temp.correspondancesLangue1["des chasseurs"],2))
    # print(desChasseurs)
    # chasseursdecoyotes = list(combinations(temp.correspondancesLangue1["chasseurs de coyotes"],2))
    # print(chasseursdecoyotes)

    for couple in deuxChasseurs:
        (string1,string2) = couple
        print(couple)
        temp = SequenceMatcher(None,string1[1],string2[1])
        temp1 = temp.get_matching_blocks()[1:]
        print(temp1)

main()