#coding: utf-8
from abc import ABCMeta, abstractmethod
import sys, sqlite3
from codecs import open
from yaml import load, dump
import re

class Decoupeur:
	__metaclass__ = ABCMeta
	@abstractmethod
	def decouper(self):
		pass
	
class DecoupeurChaine(Decoupeur):
	def __init__(self,chaine):
		self.chaine = chaine
	def decouper(self):
		return self.chaine.split()

class DecoupeurRecursif(DecoupeurChaine):
	def decouper(self, separateurs,liste=[]):
		if len(separateurs[0]) == 3:
			(separator, side, number) = separateurs[0]
			if side == "l":
				temp = self.chaine.split(separator, number)
			elif side == "r":
				temp = self.chaine.rsplit(separator, number)
		elif len(separateurs[0]) == 2:
			if not isinstance(separateurs[0][0],str):
				raise TypeError("il ne peut pas y avoir autre chose qu'un string dans cette position.")
			else:
				(separator, side) = separateurs[0]
				if side == "l":
					temp = self.chaine.split(separator)
				elif side == "r":
					temp = self.chaine.rsplit(separator)
				elif side not in ["r","l"]:
					raise TypeError("Cette position n'accepte que deux solutions 'l' ou 'r' et rien d'autre.")
		elif len(separateurs[0]) == 1:
			if not isinstance(separateurs[0][0],str):
				raise TypeError("il ne peut pas y avoir autre chose qu'un string dans cette position.")
			else:
				separator = separateurs[0][0]
				temp = self.chaine.split(separator)
		else:
			assert "il faut au moins 1 séparateur."
		if not any(x in y for x in [g[0] for g in separateurs] for y in temp) or len(separateurs) == 1:
			liste.append(tuple(temp))
		else:
			for element in temp:
				self.chaine = element
				self.decouper(separateurs[1:],liste)
		return liste

class Tableur:
	
	def __init__(self,baseNom):
		self.container = sqlite3.connect(baseNom)
		self.containerCurseur = self.container.cursor()
	
	def commandeSimple(self, commande, *args):
		self.containerCurseur.execute(commande, args)
	
	def commandeMultiple(self, commande, args):
		self.containerCurseur.executemany(commande, args)
	
	def commandeScript(self, script):
		self.containerCurseur.executescript(script)
	
	def sauvegarderDonnees(self):
		self.container.commit()
	
	def fermerBase(self):
		self.container.close()

def main():
	import argparse
	parser = argparse.ArgumentParser(
		prog="injecteurDatas.py",
		description="""
			Ce programme python prend n'importe quel fichier qu'on lui donne
			le découpe et le sauvegarde dans une ou plusieurs tables de
			bases de données.
			
			Ainsi le premier argument donné est le fichier lui-même,
			
			""",
		usage="%(prog)s [options] FICHIER_TAGGE"
	)
	
	parser.add_argument(
	"--input",
	"-i",
	type=argparse.FileType("r")
	)
	#parser.add_argument(
	#"--encoding",
	#"-e",
	#type=str
	#)
	parser.add_argument(
	"--separators",
	"-s",
	type=load,
	default=";"
	)
	
	parser.add_argument(
	"--baseName",
	"-b",
	type=Tableur
	)
	
	parser.add_argument(
	"--colnames",
	"-c",
	nargs="*"
	)

	args = parser.parse_args()
	print(args)
	
	decoupage = DecoupeurRecursif("\n".join([x.strip() for x in args.input.readlines()]))
	
	separateurs = args.separators
	colnames = args.colnames
	baseDeDonnees = args.baseName
	
	corpus = decoupage.decouper(separateurs)
	
	
	if len(corpus[0]) == len(args.colnames):
		corpusName = args.input.name.rpartition(".")[0].replace("-","_").replace(".","_")
		
		colNamesValues = ",".join(len(colnames)*"?")
		
		colNames = ",".join(["\n    {0} {1}".format(x.split()[0],x.split()[1]) for x in colnames])
		
		tableName = "CREATE TABLE IF NOT EXISTS {corpusName}({colNames});"
		
		baseDeDonnees.commandeSimple(tableName.format(corpusName=corpusName,colNames=colNames))
		
		baseDeDonnees.commandeMultiple("INSERT INTO {corpusName} VALUES ({colNamesValues})".format(corpusName=corpusName, colNamesValues=colNamesValues), corpus)
		
		baseDeDonnees.sauvegarderDonnees()
		
		baseDeDonnees.fermerBase()


main()
