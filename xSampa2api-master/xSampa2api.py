# coding: utf-8

import codecs
import yaml
import itertools
try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper
import argparse


parser = argparse.ArgumentParser(description="Translate a word in sampa to a word in API", prog="sampa2apiTranslater")

parser.add_argument('-i','--infile', type=argparse.FileType('r'), nargs='?', help="file to be copied")
parser.add_argument('-o', '--outfile', type=argparse.FileType('w+'), nargs="?", help="%(prog)s writes your translation into a file")

args = parser.parse_args()

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


def traduire_sampa2api(mot,sampa="xSampa2api.yaml"):
	"""
		Cette fonction convertit un symbole x-sampa en un vrai caractère API.
	"""
	convertisseur = yaml.load(open(sampa,'r'), Loader=Loader)
	triCles = sorted(grouperElements(convertisseur.keys()),reverse=True)
	for groupe in triCles:
		for element in groupe:
			if element in mot:
				mot = mot.replace(element,convertisseur[element]["api"])
	return mot

if args.infile:
	for element in args.infile.readlines():
		element = element.strip().split(' ')
		temp = []
		for mot in element:
			temp.append(traduire_sampa2api(mot))
		args.outfile.write(" ".join(temp)+"\n")
