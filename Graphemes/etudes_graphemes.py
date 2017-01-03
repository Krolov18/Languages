# coding: utf-8

import sys, re, os
import yaml
import subprocess
import codecs
import sqlite3
try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

#class Graphemes:
	#def __init__(self, listex):
		#"""
			#le nom listex est un nom explicite pour dire que c'est une liste pour moi.'
		#"""
		#if isinstance(listex,list):
			#self.corpus = listex
#

#dico_transform={
				#"r":"R",
				#"è":"",
				#"ò":"",
				#"":"",
				#"":"",
				#"":"",
				#"":"",
				#"":"",
				#"":""
#}
def retablirLexique():
	liste = {'è':"E", 'â':"A~", '6':"@", 'ô':"o~", 'r':"R", 'ò':"O", 'ê':"E~", 'û':"9~",'"':""}
	sortie = codecs.open(sys.argv[2],'w','utf-8')
	with codecs.open(sys.argv[1],'r','utf-8') as lexique:
		for ligne in lexique:
			ligne = ligne.strip().split(';')
			mot = ligne[1]+ligne[2]
			for lettre in mot:
				if lettre in liste:
					mot = mot.replace(lettre, liste[lettre])
			ligne[1] = mot
			sortie.write(';'.join(ligne)+'\n')

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
	print(sorted(convertisseur,reverse=True,keyfunc=len))
	for lettre in mot:
		if lettre in convertisseur[lettre]:
			mot=mot.replace(element,convertisseur[element]['api'])
	return mot
	#return [mot.replace(element,convertisseur["x_sampa"][element] for element in convertisseur['x_sampa'] if element in mot]

print(traduire_sampa2api("/home/krolev/Documents/PROJECTS_INFORMATIQUE_LINGUISTIQUE/linguistique/x-sampa2api/xSampa2api.yaml",'=\\@?\\'))


def restreindre_corpus(lexique, colonne = 0):
	with codecs.open(lexique,"r","utf-8") as fichier:
		listeSortie=[]
		for ligne in fichier:
			ligne = ligne.strip().split(';')
			if not '-' in ligne[2] or '+' in ligne[2]:
				if (len(ligne[0]) == len(ligne[1]+ligne[2].replace('"',''))) and not any(x in ligne[0] for x in ["x","-"," ","'",'y']) and not ligne[1].startswith('dZ'):
					listeSortie.append((ligne[0],ligne[1]+ligne[2].replace('"','')))
		return listeSortie


#retablirLexique()
#corpusRestraint = restreindre_corpus(sys.argv[1],1)
#for x in corpusRestraint:
	#print(x)
