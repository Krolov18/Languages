__author__ = 'korantin'

from DecoupeurRecursif import DecoupeurRecursif
import re, sys
from yaml import load, dump
from codecs import open
import pickle


with open("../RESSOURCES/lefff-2.1.txt",'r','latin-1') as lexique:
    lexicon = []
    for ligne in lexique:
        if not ligne.startswith('#'):
            lexie = {}
            temp = {}
            (form, chiffre, categorie,construction) = ligne.split('\t')
            construction = construction.replace('=',': ')
            if "@" in construction:
                construction = construction.replace('@',"a@")
            research = re.search(": '(.*)'[,\]]",construction)
            if research:
                construction = construction.replace(research.group(1),research.group(1).replace("'",'"'))
            morpho = {"morphologie": []}
            construction = load(construction)
            for element in construction:
                if isinstance(element,str):
                    morpho["morphologie"].append(element.replace("a@",''))
            construction.append(morpho)
            construction = [x for x in construction if not isinstance(x, str)]
            [temp.update(x) for x in construction]
            if "pred" not in temp: temp.update({"pred":""})
            research1 = re.search(r"(.*)_____[0-9]<(.*)>",temp["pred"])
            if research1:
                tempo = list(research1.groups())
                tempo[1] = load("{{{0}}}".format(tempo[1].replace(":",": ")))
                lexie.update({"lemme":tempo[0]})
                lexie.update({"syntaxe":tempo[1]})
            lexie.update({"forme":form})
            lexie.update({"true_cat":categorie})
            lexie.update({"chiffre":chiffre})
            del temp["pred"]
            for x,y in temp.items():
                lexie.update(dict([(x,y)]))
            lexicon.append(lexie)

with open(sys.argv[1],'wb') as stream:
    # temp = pickle.load(stream)
    # for element in temp:
#         print(element)
    dump(lexicon,stream,default_flow_style=False,allow_unicode=True)
    print(dump(lexicon, default_flow_style=False,allow_unicode=True))




class LefffExtractor:
    def __init__(self, lefff):
        self.corpus = lefff

        #Regexes
        self.etiquettesRegex = re.compile("(\w+)=(\w+|'.*>')")
        self.syntaxeRegex = re.compile("(\w+):")
        self.lemmeNumProSyntRegex = re.compile("'([a-zA-Zéèàêâôûùçîïöüë ]*)_*([0-9]*)([a-zA-Zéèàêâôûùçîïöüë]*)?(<?.*>?)?'")
        self.morphologieRegex = re.compile("@(\w+)")
        self.listeEtiquettes = ["lemme","chiffre","pronominal","fonctions"]

        # initialisations des sets
        self._etiquettes = set([])
        self._syntaxe = set([])
        self._morphologie = set([])

        # liste contenant une ligne du lefff decoupée selon les différentes méthodes de la classe
        self.lexique = []

        # boucle remplissant les trois sets.
        for tuplex in self.corpus:
            if not tuplex[0].startswith('#') and len(tuplex)==4:
                (forme,chiffre,categorie,phrases) = tuplex
                temp1 = set([x[0] for x in self.etiquettesRegex.findall(phrases)])
                temp2 = set(self.morphologieRegex.findall(phrases))
                temp3 = self.lemmeNumProSyntRegex.findall(phrases)
                if temp3 != []:
                    temp3 = set(self.syntaxeRegex.findall(temp3[0][-1]))
                else:
                    temp3 = set(temp3)
                self.updateEtiquettes(temp1)
                self.updateMorphologie(temp2)
                self.updateSyntaxe(temp3)
        print(self.getEtiquettes())
        print(self.getSyntaxe())
        print(self.getMorphologie())



    def getEtiquettes(self):
        return self._etiquettes
    def updateEtiquettes(self,set):
        self._etiquettes |= set

    def getSyntaxe(self):
        return self._syntaxe
    def updateSyntaxe(self,set):
        self._syntaxe |= set

    def getMorphologie(self):
        return self._morphologie
    def updateMorphologie(self,set):
        self._morphologie |= set

    etiquettes = property(fget=getEtiquettes,fset=updateEtiquettes,doc="etiquettes property")
    syntaxe = property(fget=getSyntaxe,fset=updateSyntaxe,doc="syntaxe property")
    morphologie = property(fget=getMorphologie,fset=updateMorphologie,doc="morphologie property")

    def attribuerValeurs(self,chaine):
        morpho = self.morphologieRegex.findall(chaine)
        etiquettes = dict(self.etiquettesRegex.findall(chaine))
        etiquettes.update(dict(zip(self.listeEtiquettes,self.lemmeNumProSyntRegex.search(etiquettes["pred"]).groups())))
        etiquettes.pop("pred")

def main():
    pass

# def main():
#     temp = DecoupeurRecursif(open(sys.argv[1],encoding="latin1").read())
#     temp.decouper(separateurs=[["\n"],["\t"]])
#     analyse = LefffExtractor(temp.liste)


if __name__=="__main__":
    main()