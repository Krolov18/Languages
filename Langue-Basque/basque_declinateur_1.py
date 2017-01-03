# ouvrir la liste de phrases,
# ajouter mot au lexique (mots.txt)
# découper mot de sa désinence
# actualiser le lexique
#
# pour générer de nouvelles formes, on cherche
# l'absolutif indéfini, on applique les désinence sans oublier la ou les règles d'épenthèses.
#
#
# Tandis que dans un cas on génère des formes casuelles, de l'autre, on interroge la base pour savoir si la forme
# proposée est correctement formée.#
# #

import sqlite3
import csv
import codecs
import sys

fichier = sys.argv[1]
connection = sqlite3.connect(fichier)
curseur = connection.cursor()



def decliner_nom(nom,anime=False,cas="ABS",nombre="INDEF"):
	"""
	Cette fonction prend un lexème nu de toute marque
	et par l'argument de cas, se voit attribué une marque.
	Cette fonction lie donc une désinence (le cas) à un lexème (base lexicale).
	:param nom: string
	:param cas: string
	:return: string
	NB = ["INDEF","DEF_SG","DEF_PL_EXCL","DEF_PL_INCL"]
	"""
	if anime == True:
		curseur.execute("""SELECT {0},nb FROM anime WHERE nb ='{1}'""".format(cas,nombre))
		declinaison = list(curseur.fetchone())
		declinaison.append(cas)
		declinaison.insert(0,nom)
		return declinaison
		
		# (base,decl,cas,nombre)
		# (mikel,ek,erg,indef)
	else:
		curseur.execute("""SELECT {0} FROM inanime WHERE nb = '{1}'""".format(cas,nombre))
		declinaison = curseur.fetchone()
		nb = curseur.fetchone()

nbs = ["INDEF","DEF_SG","DEF_PL_EXCL","DEF_PL_INCL"]
decls = ["ABS","ERG","DAT","GEN_POSS","SOCIA","DESTIN","MOTIV","INSTRU","INES","ABLA","AD","AD_TERM","AD_DIREC","AD_DESTIB"]

def trouver_declinaison():
	# liste = [("","","")]
	dico = {}
	for decl in decls:
		curseur.execute("""select ABS,ERG,DAT,GEN_POSS,SOCIA,DESTIN,MOTIV,INSTRU,INES,ABLA,AD,AD_TERM,AD_DIREC,AD_DESTIB from anime""")
		dico.update({"anime":curseur.fetchall()})
		curseur.execute("""select ABS,ERG,DAT,GEN_POSS,SOCIA,DESTIN,MOTIV,INSTRU,INES,ABLA,AD,AD_TERM,AD_DIREC,AD_DESTIB from inanime""")
		dico.update({"inanime":curseur.fetchall()})
	return dico

print(trouver_declinaison())


#for decl in decls:
#	for nb in nbs:
#		print(decliner_nom("gizon",anime=True,cas=decl,nombre=nb))
#print("gizon",decliner_nom("gizon",anime=True,cas="INSTRU",nombre="DEF_SG"))
