# -*- coding: utf-8

from pattern.web import Wikipedia
import sys
import yaml
from nltk.util import bigrams

def element_inString(string, liste):
	"""
		on verifie si un élément de liste commence le string.
	"""
	for pays in liste:
		if string.startswith(pays.encode('utf-8')):
			return True


def recherche_wikipedia(recherche, language):
	"""
		Fonction principale de ce script python 27 qui fait une requête
		wikipedia afin de récupérer les informations sur une page
		wikipedia.
		
		La fonction n'a formatté que les informations des recherches
		"fr" et "en" et plus précisément les sections pour "fr"
		Fiche technique, distribution, voix françaises et originales
		et en "en" le casting. Cette fonction peut évidemment être
		étoffée pour récupérer plus d'informations.
	"""
	datas = yaml.load(open("/home/krolev/Documents/Projet_media/BIBLIOTHEQUES/formats_acceptes.yaml"))
	engine = Wikipedia(language=language)
	searching = engine.search(recherche)
	Sections = searching.sections
	metadata = {}
	def fonction(part=True,sepa = ":"):
		"""
			fonction interne à recherche wikipedia qui permet de mettre
			en forme le texte récupéré pour être formatté avant le
			passage dans YAML.load()
		"""
		temp = [x.strip() for x in section.content.replace('* ','').split('\n') if x != u""]
		liste = []
		for element in temp:
			element = element.encode('utf-8')
			if part:
				(cle,sep,attr) = element.partition(sepa)
			else:
				(cle,sep,attr) = element.rpartition(sepa)
			attr = attr.strip()
			cle = cle.strip()
			if "'" in cle:
				attr = attr.replace("'","''")
			if "'" in attr:
				attr = attr.replace("'","''")
			if ":" in cle:
				cle = cle.replace(':','--')
			if ":" in attr:
				attr = attr.replace(":","--")
			element = " ".join([x for x in [cle+sep, attr] if x != '""'])
			if element_inString(element,datas["countries"]):
				element = " "+element
			elif (not ":" in element):
				element = " "+element
			liste.append(element)
		return liste
	
	if language == "fr":
		for section in Sections:
			if section.title == u"Fiche technique":
				metadata.update({"Fiche_technique":yaml.load("\n".join(fonction()[1:-1]))})
			elif section.title == u"Distribution":
				temp = fonction()
				if len(temp) != 1:
					metadata.update({"Distribution":yaml.load("\n".join(fonction(part=False)[1:-1]))})
			elif section.title == u"Voix françaises":
				metadata.update({u"Voix françaises":yaml.load('\n'.join(fonction()[1:-1]))})
			elif section.title == u"Voix originales":
				metadata.update({"Voix originales":yaml.load('\n'.join(fonction()[1:-1]))})
	if language == "en":
		for section in sections:
			if section.title == 'Cast':
				liste = []
				for element in fonction(sepa="as")[1:-1]:
					(cle, sep, val) = element.partition('as')
					element = cle+":"+val
					liste.append(element)
				metadata.update({"Casting":yaml.load('\n'.join(liste))})
	#return metadata
	return yaml.dump(metadata, default_flow_style = False, allow_unicode = True)

recherche = sys.argv[1]
language = sys.argv[2]
metadata = recherche_wikipedia(recherche,language)

print(metadata)
