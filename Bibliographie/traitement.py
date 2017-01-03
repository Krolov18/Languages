# coding: utf-8

from bs4 import BeautifulSoup as bs
from codecs import open

with open("/home/korantin/PycharmProjects/Languages/Bibliographie/Distributed-Morphology-Bibliography.html",'r','latin1') as fichier:
	temp = bs(fichier,"lxml")
	# (reference, lien)
	#print(temp)
	for ref in temp.find_all('p'):
		for a in ref.find_all('a'):
			if "href" in a.attrs:
				print(ref.text.strip().replace('\t',' ').replace('\n',' '), a.get('href').strip())

def type(type, champs):
	return "@{type}{{\nchamps\n}}".format(type=type, champs="\n".join())
def champ(champ, contenu):
	return "{champ}={{contenu}}".format(champ=champ, contenu=contneu)
	


#@type{champs}
####typeDeDocument entre parenthèses champs requis)
#article (author, title, journal, year)
#book (author/editor, title, publisher, year)
#booklet (title)
#conference (author, title, booktitle, year)
#inbook (author/editor, title, chapter/pages, publisher, year)
#incollection (author, title, booktitle, year)
#inproceedings (author, title, booktitle, year)
#manual (author, title, booktitle, year)
#mastersthesis (author, title, school, year)
#misc ()
#phdthesis (author, title, school, year)
#proceedings (title, year)
#techreport (author, title, institution, year)
#unpublished (author, title, note)

#champ={contenu}
####champs
#label: reference pour la citation
#address : L'adresse de l'éditeur.
#abstract : Résumé de l'article.
#annote : Une annotation.
#author : Nom(s) puis prénom(s) des auteurs séparés par and. Exemple : author = {DO, John and DUPOND, Marc}
#booktitle : Le titre du livre.
#chapter : Le numéro de chapitre.
#crossref : La clé d'une référence croisée.
#edition : L'édition du livre.
#editor : Le nom de l'éditeur scientifique.
#eprint : La spécification d'un publication électronique.
#howpublished : Comment il a été publié, si ce n'est pas avec une méthode standard.
#institution : L'institution impliquée dans la publication (pas forcément l'éditeur).
#journal : La revue ou le magazine dans lequel le travail a été publié.
#key : Un champ caché utilisé pour spécifier ou remplacer l'ordre alphabétique des entrées (quand "author et "editor" ne sont pas présents).
#month : Le mois de la création ou de la publication.
#note : Informations diverses.
#number : Le numéro du journal ou du magazine.
#organization : Le sponsor d'une conférence.
#pages : Les numéros de pages, séparés par des virgules ou sous forme d'intervalles.
#publisher : Le nom de la maison d'édition.
#school : L'école dans laquelle la thèse a été écrite.
#series : La collection dans laquelle la livre a été publié.
#title : Le titre du document.
#type : Le type.
#url : L'adresse URL.
#volume : Le volume, dans le cas où il y a plusieurs volumes.
#year : L'année de publication (ou de création s'il n'a pas été publié).

