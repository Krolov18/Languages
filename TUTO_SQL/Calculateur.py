# coding: utf-8
from Tableur import Tableur
import argparse
from bs4 import BeautifulSoup as bs
from codecs import open

def main():
	parser = argparse.ArgumentParser(
		prog="Calculateur.py",
		description="""
			A partir de plusieurs tables d'une base de données,
			ce script permet de faire les deux calculs d'ambiguité et
			l'affichage par nombre d'occurences décroissant.
		""",
		usage="%(prog)s [options] BDD"
	)
	parser.add_argument(
		"--input",
		"-i",
		help="Nom de la base de données à utiliser.",
		type=Tableur
	)
	parser.add_argument(
		"--ambigCatVoc",
		"-cv",
		help="Calcul du taux moyen d'ambiguité sur formes distinctes (par 'type')",
		action="store_true"
	)
	parser.add_argument(
		"--ambigOccCorpus",
		"-co",
		help="Calcul du taux moyen d'ambiguité sur les occurrences de formes (par 'token')",
		action="store_true"
	)
	parser.add_argument(
		"--afficher",
		"-af",
		help="Afficher les N premières formes les plus fréquentes du corpus, dans l'ordre décroissant",
		type=int,
		default=100
	)
	
	args = parser.parse_args()
	print(args)
	
	nbMaxVirg = '{0:.3f}'
	if args.ambigCatVoc:
		commande = "SELECT SUM(nbCategories) FROM corpusCalcule WHERE categories != 'PONCT'"
		#commande = "SELECT SUM(nbCategories) FROM corpusCalcule"
		args.input.commandeSimple(commande)
		numerateur = args.input.containerCurseur.fetchone()[0]
		
		commande = "SELECT lenVocabulaire FROM metadatasCorpus"
		args.input.commandeSimple(commande)
		denominateur = args.input.containerCurseur.fetchone()[0]
		resultat = numerateur/denominateur
		
		print("Nb moyen de catégories par forme distincte:", nbMaxVirg.format(resultat))
	
	if args.ambigOccCorpus:
		commande = "SELECT SUM(nbCategories*nbFormes) FROM corpusCalcule WHERE categories != 'PONCT'"
		#commande = "SELECT SUM(nbCategories*nbFormes) FROM corpusCalcule"
		args.input.commandeSimple(commande)
		numerateur = args.input.containerCurseur.fetchone()[0]
		
		commande = "SELECT lenCorpus from metadatasCorpus"
		args.input.commandeSimple(commande)
		denominateur = args.input.containerCurseur.fetchone()[0]
		resultat = numerateur/denominateur
		
		print("Nb moyen de catégories par occurrence de forme:", nbMaxVirg.format(resultat))
	
	commande = """
		SELECT * FROM corpusCalcule
		ORDER BY nbFormes DESC;
	"""
	args.input.commandeSimple(commande)
	extraction = args.input.containerCurseur.fetchall()
	
	sortie = open("fichier.html","w","utf-8")
	table = """<table>{lignes}</table>"""
	header = """<th>{columnName}</th>"""
	tableRow = """<tr>{tableDatas}</tr>"""
	tableData = """<td align="center">{data}</td>"""
	
	temp = []
	temp.append('<meta charset="UTF-8">')
	THColonnes = ["forme","categorie","nbCategories","nbFormes","nbFormesParCat"]
	colNames = "".join([header.format(columnName=colonne) for colonne in THColonnes])
	temp.append(colNames)
	for i in range(args.afficher):
		datas = [tableData.format(data=donnee) for donnee in extraction[i]]
		tableRows = tableRow.format(tableDatas="".join(datas))
		temp.append(tableRows)
	tableFinal = table.format(lignes="".join(temp))
	soup = bs(tableFinal,"html")
	sortie.write(soup.prettify())

if __name__=="__main__":
	main()
