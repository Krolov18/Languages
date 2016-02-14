# coding=utf-8

import re
import argparse
import codecs
from itertools import *
from nltk import ngrams
import string
import yaml

parser = argparse.ArgumentParser()
parser.add_argument('corpus_kalaba')
args = parser.parse_args()
corpus_kalaba = args.corpus_kalaba


# longueur
# position
# contexte
# lettre


phrase = "kik jigib kimaninit dSarrivu lud Nulak lagoboddu"
listex = phrase.strip().split(' ')
#print(groups(listex,len))


#corpus composé de phrases, phrases composées de ngrams, ngrams composés de lettres.

# Fonction1: création du lexique (Ngrams)
def lexique(phrase):
	"""liste des ngrams du corpus rangés par longueurs de ces derniers."""
	data=[]
	phrase=phrase.strip().split()
	for i in range(len(phrase)):
		for gram in ngrams(phrase,i+1):
			if gram not in data:
				data.append(gram)
	lexique=groups(data,len)
	return lexique

def couperSequence(strin):
	if " " in strin:
		return strin.strip().split()
	else:
		return list(strin)

def obtenirCorpus(liste):
	nvList = []
	for element in liste:
		elList = couperSequence(element)
		for el in elList:
			if el not in nvList:
				nvList.append(el)
	return nvList

def grouperElements(liste, function=len):
	"""
		fonctions qui groupe selon la fonction qu'on lui donne.
		Ainsi pour le kalaba comme pour les graphèmes, nous aurons
		besoin de la longueur,
	"""
	lexique=[]
	data=sorted(liste, key=function)
	for k,g in groupby(data, function):
		lexique.append(list(g))
	return lexique

#def PairerMinimales(liste):
	
with codecs.open(corpus_kalaba,"r",encoding="utf-8") as kalaba:
	kalaba = [phrase.strip() for phrase in kalaba]
	mots = obtenirCorpus(kalaba)
	alphabet = obtenirCorpus(mots)
	print(mots)
	listLongueur = grouperElements(mots)
	liste = []
	for element in listLongueur:
		for x in grouperElements(element,None):
			liste.extend(x)
			print(liste)
		liste = []
