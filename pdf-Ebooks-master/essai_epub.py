# coding: utf-8
import sys,codecs

### Traitement des ebooks

import zipfile

#def get_epub_content(fname):
	#ziip = zipfile.ZipFile(fname)
	#txt = ziip.read('OEBPS/*.xhtml')
#get_epub_content(sys.argv[1])

### Traitement des fichiers pdf

# renommer_fichier
# pdf2xml
# xml2yaml

translate = {"ﬀ":"ff","“":'"',"’’":'"',"":"","":""}

#
import yaml
from pypdf2xml import pdf2xml
from bs4 import BeautifulSoup as bs

def attribuer(string, noeud, attributs):
	"""
		string est l'élément qui sera mis entre balises.
		noeud sera le nom du noeud dans lequel sera string
		attributs est un dictionnaire.
		
	"""
	nouage = "<{0} {1}>{2}</{0}>"
	attrs = yaml.dump(attributs).strip("\n{}").replace(":","=").replace(",","")
	return nouage.format(noeud,attrs,string)

fichier_in = sys.argv[1]
(sortie,sep,extension) = fichier_in.rpartition('.')

fichier_xml = pdf2xml(open(fichier_in,"r")).splitlines()
for ligne in fichier_xml:
	print(ligne)
#soup = bs(fichier_xml,"xml")
#print(soup.prettify())
#with codecs.open(sortie+sep+"xml","w") as ecriture:
	#for ligne in fichier_xml:
		#ecriture.write(ligne+"\n")
