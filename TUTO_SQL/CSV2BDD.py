#coding: utf-8
from DecoupeurRecursif import DecoupeurRecursif
from Tableur import Tableur
from codecs import open
#from yaml import load, dump
#from pickle import load, dump
import argparse

def CSV2BDD():
	"""
		Cette fonction prend n'importe quel fichier taggé
		avec lequel vous fournissez les séparateurs pour le découpage.
		
		Ensuite on fournit à cette fonction le nom de la BaseDeDonnees,
		puis un script SQL.
		
		Ici cette fonction et le script SQL utilisé est visé au format
		de emea-fr.brown mais on peut imaginer un upgrade
		de cette fonction qui abstrait les formats de fichiers afin de
		recevoir n'importe quel format.
		
		l'option des colonnes sera pour plus tard.
	"""
	parser = argparse.ArgumentParser(
		prog="CSV2BDD.py",
		description="""
			Ce script prend un corpus au format CSV, le transforme en base de données,
			et peut permettre à l'utilisateur d'interroger cette base de données.
		""",
		usage="%(prog)s [options] FICHIER_TAGGE"
	)
	
	parser.add_argument(
		"--input",
		"-i",
		help="Cet argument prend le nom du corpus à découper.",
		type=argparse.FileType("r")
	)
	
	parser.add_argument(
		"--separators",
		"-s",
		nargs="?",
		help="""Cet argument 'est lu par un programme qui transforme du string en structure python.
				donc quelque chose comme '[carton,carotte,conserve]' donnera ['carton', 'carotte', 'conserve']
				un separateur peut contenir jusqu' trois élément: d'abord un séparateur, la lettre "l" ou "r"
				suivant le côté par lequel on veut découper puis un chiffre qui déterminera le nombre de fois
				qu'il faut découper.
				
				Exemple:
				
				[[" ","r",2],["\t"]]
				
				Cet exemple est composé de deux ensembles (deux séparateurs). le premier qui sature les possibilités (3)
				va donc découper sur les espaces (" ") en partant de la droite ("r") et faire l'action que deux fois puis
				le second ensemble va découper sur les tabulations ("\t")
				""",
		default=[["\n"],[" "],["/","r",1]]
	)
	
	parser.add_argument(
		"--baseName",
		"-b",
		help="Cet arguent prend le nom de la base de données à ouvrir.",
		type=Tableur
	)
	
	parser.add_argument(
		"--script",
		"-sc",
		help="Ensemble de plusieurs commande SQL qui sera donné au module sqlite3",
		type=argparse.FileType("r")
	)
	
	parser.add_argument(
		"--colnames",
		"-c",
		help="""Cet argument prend autant d'arguments que nécessaires, il représentera
				le nom des colonnes de la table qui sera créée.""",
		nargs="*"
	)

	args = parser.parse_args()
	print(args)

	decoupage = DecoupeurRecursif(args.input.read())

	separateurs = args.separators

	colnames = args.colnames

	baseDeDonnees = args.baseName
	
	tempCorpus = decoupage.decouper(separateurs)
	corpus = [couple for couple in tempCorpus if "" not in couple]
	
	baseDeDonnees.commandeSimple("""
		CREATE TABLE IF NOT EXISTS corpusDatas (
			forme TEXT,
			categorie TEXT
		);
	""")
	
	baseDeDonnees.commandeMultiple("INSERT INTO corpusDatas VALUES (?,?)", corpus)
	
	if args.script:
		temporary = "\n".join([x.strip("\n") for x in args.script.readlines()])
		baseDeDonnees.commandeScript(temporary)
	baseDeDonnees.sauvegarderDonnees()
	baseDeDonnees.fermerBase()

if __name__ == "__main__":
	CSV2BDD()
