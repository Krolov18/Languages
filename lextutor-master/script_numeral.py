# coding: utf-8

from bs4 import BeautifulSoup
import sys, codecs, string
from urllib.parse   import *
from urllib.request import urlopen
import sqlite3
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


corpora = ["Fr_150k_parle.txt","Fr_le_monde.txt","Fr_Maupassant.txt","",""]

def verif_lexique(curseur, mot):
	"""
		Envoyer une requête (forme graphique d'un lexème à la base et renvoie sa catégorie grammaticale. 
	"""
	search = curseur.execute('''SELECT categorie from lexique380 where ortho = ?''', [mot])
	cat = search.fetchone()
	if not cat is None:
		return {mot:cat[0]}

def changer_caracteres(chaine):
	"""
		Remplacement de caractères. Problèmes d'encodage à résoudre...
	"""
	for element in chaine:
		chaine = chaine.replace("\\xe0","à")
		chaine = chaine.replace("\\xe9","é")
		chaine = chaine.replace("\\xe8","è")
		chaine = chaine.replace("\\xe7","ç")
		chaine = chaine.replace("\\xf4","ô")
		chaine = chaine.replace("\\xea","ê")
		chaine = chaine.replace("\\'","'")
		chaine = chaine.replace("\\xe2","â")
		chaine = chaine.replace("\\xfb","û")
		chaine = chaine.replace("\\xca","É")
		chaine = chaine.replace("\\xc9","Ê")
		chaine = chaine.replace("\\xf9","ù")
		chaine = chaine.replace("\\xef","ï")
		chaine = chaine.replace("\\xee","i")
		
	return chaine

def generer_lien(mot, lexique):
	"""
		retourne une liste de liens.
		'mot': [contgauche, contdroit]
	"""
	dbase = sqlite3.connect(lexique)
	curseur = dbase.cursor()
	commande = "http://www.lextutor.ca/cgi-bin/conc/wwwassocwords.pl?lingo=French&KeyWordFormat=&Maximum=10003&LineWidth=100&Gaps=no_gaps&store_dic=&is_refire=true&Fam_or_Word=&Source=http%3A%2F%2Fwww.lextutor.ca%2Fconc%2Ffr%2F&unframed=true&SearchType=equals&SearchStr={0}&Corpus=Fr_le_monde.txt&ColloSize=&SortType={1}&AssocWord=&Associate={1}"
	droite = commande.format(quote_plus(mot,encoding="ISO 8859-1"),"right")
	gauche = commande.format(quote_plus(mot,encoding="ISO 8859-1"),"left")
	return {mot:[{"gauche":[verif_lexique(curseur,mot) for mot in envoyer_requete(gauche)]},{"droite":[verif_lexique(curseur,mo) for mo in envoyer_requete(droite)]}]}

def decouper_mot(mot):
	"""
		Il découpe un string sur "=" et renvoie le premier élément de la liste.
	"""
	return mot.split('=')[0].strip(string.punctuation)

def envoyer_requete(lien):
	"""
		Cette fonction permet de récupérer le résultat de la recherche sur Lextutor.
	"""
	ouvertureLien = urlopen(lien)
	lectureLien = str(ouvertureLien.read())
	parseur = BeautifulSoup(lectureLien)
	texte = parseur.find('textarea').text
	liste = []
	for mot in changer_caracteres(texte).split(' '):
		mot = decouper_mot(mot)
		if mot not in liste:
			liste.append(mot)
	return sorted(liste)


# {mot:{"gauche":[{"mot":"categorie"}],"droite":[{"mot":"categorie"}]}}



def main():
	sortie = codecs.open(sys.argv[1],"w","latin1")
	lexique = sys.argv[2]
	listemots = ["zéro", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "plusieurs", "nul", "personne", "un", "une", "chacun", "chacune", "aucun", "aucune", "le", "la", "les", "des", "ce", "cet", "cette", "ces", "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses", "notre", "nos", "votre", "vos", "leur", "leurs", "gentil", "gentille", "gentils", "gentilles", "pris", "prise", "pris", "prises"]
	dump([generer_lien(mot, lexique) for mot in listemots],sortie, allow_unicode=True, default_flow_style=False)

if __name__ == "__main__":
	main()
