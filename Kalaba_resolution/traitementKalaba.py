import re
from bs4 import BeautifulSoup as bs
from sys import argv
from codecs import open
from itertools import combinations, islice




class FormeurTXT:
    def __init__(self,xmlFile):
        self.entree = bs(open(xmlFile),"xml")
        self._phrases = []
        self.recupererTexte()
        self.genererCorpus()

    def recupererTexte(self):
        for text in self.entree.find_all("text"):
            if not any(x in text.string for x in ['Imaginez','nées','−→ ',"mission","chaque","6","régissent","indiqué","phénomènes","1","2","3","5","4","(",")","Kalaba","lègues,","Corpus"]):
                self._phrases.append(text.string)
    def getPhrases(self):
        return self._phrases
    def genererCorpus(self):
        francais = [phrase for phrase in islice(self._phrases,1,len(self._phrases),2)]
        kalaba = [phrase for phrase in islice(self._phrases,0,len(self._phrases),2)]
        self._corpus = list(zip(francais,kalaba))
    def getCorpus(self):
        return self._corpus
    phrases = property(fget=getPhrases)
    corpus = property(fget=getCorpus)

def longest_common_string(string1,string2):
    set1 = set(string1[begin:end] for (begin,end) in combinations(range(len(string1)+1), 2))
    set2 = set(string2[begin:end] for (begin,end) in combinations(range(len(string2)+1), 2))
    common = set1&set2
    maximal = [com for com in common if sum((s.find(com) for s in common)) == -1 * (len(common)-1)]
    return [(s,string1.index(s),string2.index(s)) for s in maximal]

def main():
    temp = FormeurTXT(argv[1])
    for x in temp.getCorpus():
        print(x)

if __name__=="__main__":
    main()