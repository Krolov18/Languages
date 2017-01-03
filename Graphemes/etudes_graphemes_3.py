# coding: utf-8

import re, os, sys, itertools
#import yaml
#import subprocess
import codecs
#import sqlite3
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from yaml.representer import Representer
from collections import *
from yaml import *

class lireBDLexique:
	"""
		Classe qui gère *bdlexique*
		Restriction, recherche, mise en forme...
	"""
	def __init__(self, corpus):
		self.corpus = corpus
	
	def restreindreCorpus(self, *args):
		"""
			Fonction qui permet de récuper certaines colonnes de bdlexique.
			la sortie est une liste de tuple. tuple qui contient la ou les colonnes sélectionnées.
		"""
		if not all(isinstance(element,int) for element in args):
			raise KeyError('Il ne faut que des integers.')
		else:
			self.corpusRestreint=[]
			for ligne in self.corpus:
				temp = []
				for indice in args:
					temp.append(ligne[indice])
				self.corpusRestreint.append(tuple(temp))
			return self.corpusRestreint

	def entourerElement(self, debut, fin=None):
		"""
			Cette méthode permet d'entourer un string d'éléments qu'on veut,
			il suffit de passer en argument debut et fin un string.
		"""
		if not fin is None:
			return [tuple('{debut}{0[0]}{fin}_{debut}{0[1]}{fin}'.format(element,debut=debut,fin=fin).split('_')) for element in self.corpus]
		else:
			return [tuple('{debut}{0[0]}{fin}_{debut}{0[1]}{fin}'.format(element,debut=debut,fin=debut).split('_')) for element in self.corpus]

		
	def rechercherDansCorpus(self, recherche = "^a....$", colonne = 0):
		"""
			La recherche est automatiquement passé à re.search().
		"""
		listex=[]
		for ligne in self.corpus:
			if recherche is ligne[0]:
				return (ligne[0],ligne[1])
				#listex.append((ligne[0],ligne[1]))
		#return listex

	def chercherInCorpus(self, liste, *args):
		"""
			bdlexique:
			abaissez;abEsez;z";V;2P;pi;abaisser;L23;493;1804;53;7
			graphie phonologie liaison catégorie personne+nombre TAM lemme ch1 ch2 ch3 ch4 ch5
		"""
		return [ligne[0:2] for ligne in self.corpus if all(x in ligne for x in args)]


def traduire_sampa2api(fichier,mot):
	"""
		Cette fonction convertit un symbole sampa en un caractère API.
		Améliorer la fonction en triant convertisseur par longueur et chercher les éléments des plus
		longs au plus court pour une conversion optimale ainsi si on a:
		'=\@?\'
		comme chaque symbole pris de manière détachée existe dans la base il faut donc
		chercher du plus long au plus petit pour arriver de '=\@?\' (soit ['=\', '@', '?\'])
		à
	"""
	convertisseur = yaml.load(open(fichier,'r'), Loader=Loader)
	for lettre in mot:
		if convertisseur[lettre]:
			mot = mot.replace(lettre,convertisseur[lettre]['api'])
	return mot

class Graphemes(lireBDLexique):
	def __init__(self):
		self.contextesEnrichis = []
		self.lexiqueReglesMots = {} # dictionnaire par clé (mots)
		self.lexiqueReglesPositions = {}


	def __repr_regles__(self):
		return ['{0[0]}: {0[1]} --> {0[2]} | {0[3]} _ {0[4]}'.format(regle) for regle in self.regles]


def entourer_string(string, debut="#", fin="#"):
	return "{debut}{0}{fin}".format(string, debut=debut, fin=fin)

def constituer_regles(tupl):
	regles = []
	graphie = entourer_string(tupl[0])
	phonie = entourer_string(tupl[1])
	if len(graphie) == len(phonie):
		for position, lettre in enumerate(graphie):
			if not "#" is lettre:
				rule = [position-1, graphie[position], phonie[position], graphie[position-1],graphie[position+1]]
				regles.append(rule)
		return {tupl[0]:regles}
	else:
		for position, lettre in enumerate(graphie):
			if not "#" is lettre:
				rule = [position-1, graphie[position], graphie[position-1],graphie[position+1]]
				regles.append(rule)
		return {tupl[0]:regles}

def constituer_motRegles(tuplList, dictionnaire):
	i=0
	for tupl in sorted(tuplList):
		regle = constituer_regles(tupl)
		i+=1
		for cle in regle.keys():
			if not cle in dictionnaire:
				dictionnaire.update(regle)
			elif ( cle in dictionnaire ) and ( dictionnaire[cle] != list(regle.values()) ):
				dictionnaire[cle+str(i)] = list(regle.values())[0]

def constituer_positionsRegles(dico, sortie):
	for cle in dico:
		length = len(cle.strip('123456789'))
		#print(cle, len(cle.strip('123456789')))
		if length not in sortie:
			for indice, position in enumerate(dico[cle]):
				if indice not in sortie[length]:
					sortie[length][indice]=[position]
				else:
					#if position not in sortie[length][indice]:
					sortie[length][indice].append(position)
		else:
			for indice, position in enumerate(dico[cle]):
				if indice not in sortie[length]:
					sortie[length][indice]=[position]
				else:
					if position not in sortie[length][indice]:
						sortie[length][indice].append(position)
	return sortie

def grouperElements(liste, function=len):
	"""
		fonctions qui groupe selon la fonction qu'on lui donne.
		Ainsi pour le kalaba comme pour les graphèmes, nous aurons
		besoin de la longueur,
	"""
	lexique=[]
	data=sorted(liste, key=function)
	for k,g in itertools.groupby(data, function):
		lexique.append(list(g))
	return lexique

class InfiniteDict(defaultdict):
	"""
		Cette petite classe permet de créer un dictionnaire "théoriquement" infini.
		Cela signifie qu'une fois instanciée, on peut faire un appelle de clé sans que celles ci
		soient au préalables déjà existentes.
		sans cette classe cela:
		
		dico = {}
		dico["&"]["&"]["&"]["&"]=45
		
		produit:
		
		Traceback (most recent call last):
		File "<stdin>", line 1, in <module>
		KeyError: '&'

		tandis que:
		
		dico = InfiniteDict()
		dico["&"]["&"]["&"]["&"]=45
		
		produit:
		
		defaultdict(<class '__main__.InfiniteDict'>, {'&': defaultdict(<class '__main__.InfiniteDict'>, {'&': defaultdict(<class '__main__.InfiniteDict'>, {'&': defaultdict(<class '__main__.InfiniteDict'>, {'&': 45})})})})
		
	"""
	def __init__(self):
		defaultdict.__init__(self, self.__class__)

# cette ligne permet de rétablir le type InfiniteDict en dict quand 
# utilise yaml bien entendu.
add_representer(InfiniteDict, Representer.represent_dict)

LengthPostionsRegles = InfiniteDict()

motRegles = {}
corpusTemp = codecs.open("./RESSOURCES_LEXICALES-master/BDLexique/lexiqueRepare.txt","r","utf-8")
corpus = [x.strip().split(';') for x in corpusTemp]
bdlexique = lireBDLexique(corpus)
corpora = bdlexique.restreindreCorpus(0,1)


lexiqueSansRep = list(set(corpora)) # liste de tuple binaires (graphie, phonologie(forme profonde))

motReglesRemplissage = constituer_motRegles(lexiqueSansRep, motRegles)

positionsRegles = constituer_positionsRegles(motRegles, LengthPostionsRegles)



print(dump(positionsRegles[2], Dumper=Dumper, allow_unicode=True, default_flow_style=False))




