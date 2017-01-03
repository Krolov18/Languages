__author__ = 'krolev'

import os
import shlex
import argparse
import codecs
import subprocess
import re
import string
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from pyinotify import ProcessEvent, Notifier, ALL_EVENTS, WatchManager
import sqlite3

caractère_special = ('&#160;: ', ';')

net="""
class Nettoyage():
    def __init__(self, objet):
        self.objet = objet

    def supprimer_elements(self,*args):
        for element in args:
            if element in self.objet:
                self.objet.remove(element)
        return self.objet

    def supprimer_caracteres(self,table,sep=' '):
        return "".join([element for element in self.objet.translate(table).split(sep) if element != ''])
"""



###### Charsets de substitution
changer_PointEspace2Tiret6 = str.maketrans('. ', '--')
changer_ponctuation2tiret6 = str.maketrans(string.punctuation + ' ', '-' * (len(string.punctuation) + 1))
changer_ponctuation2tiret8 = str.maketrans(string.punctuation + ' ', '_' * (len(string.punctuation) + 1))
changer_ponctuation2space = str.maketrans(string.punctuation, ' ' * (len(string.punctuation)))
#######



def nommer_lien_wiki_fre(langue, string):
    return 'http://{langue}.wikipedia.org/wiki/{string}'.format(langue=langue, string=string.lower())
#def nommer_lien_wiki_eng(string):
    #nvString = 'http://en.wikipedia.org/wiki/{0}'.format(string).lower()
    #return nvString


def selectionner_donnees_wikipedia(database):
	
    tempList = [liste[liste.index(element) + 1] for element in liste if
                ("Titre&#160;" in element or "Titre Original&#160;" in element) or
                ("Réalisateur&#160;" in element) or
                ("Société de production&#160;" in element or "Sociétés de production&#160" in element) or
                ("Musique&#160;" in element)]


def recolter_donnees_wikipedia(liste, recherche):
	"""
	Récupération de sdonnées précises sur Wikipédia.
	"""
	ouvertureLien = urllib.request.urlopen(string)
	parseur = Beautifulsoup(ouvertureLien)
	print(parseur.prettify())
	print()
	rep = input("Ces données vous satisfaient-elles? ")
	oui = ["1","o","y","yes","oui"]
	non = ["0","n","no","non"]
	while rep not in oui or non:
		input("Je n'ai pas compris votre choix.\nVeuillez tapez (y or n) à nouveau. Merci!")
	if rep.lower() in non:
		nvOuv = input("Tapez le lien exact vers le site du média svp: ")
		ouvertureLien = urllib.request.urlopen(nvOuv)
		parseur = BeautifulSoup(ouvertureLien)
	elif rep.lower() in oui:
		list(recherche)
		

def selectionner_mediaInfo(liste):
    """
	Mediainfo nous fournit des informations que nous allons mettre dans un format plus utilisable.
	voir à terme de faire un dictionnaire de dictionnaire:
	
	"""
    if isinstance(liste, list):
        temp = [re.sub(' *: ', ';', element) for element in liste]
        return dict([(x.split(';')) for x in temp])
        #return [element.split(";")[1]
                       #for element in temp if
                       #(element.split(";")[0] == "Track name") or
                       #(element.split(";")[0] == "Track name/Position") or
                       #(element.split(";")[0] == "Album") or
                       #(element.split(";")[0] == "Performer") or
                       #(element.split(";")[0] == "Recorded date") or
                       #(element.split(";")[0] == "Sampling rate")]
    else:
        print("Ce doit être une liste pas un(e) {0}".format(type(liste)))





def formatter_mediaInfo(liste):
    return [re.sub(' *: ', ';', element) for element in liste]

def nettoyer_lignes_parsees(liste):
    """
		Cette fonction va parser du code HTML. Il va simplement sélectionner une zone
		par la balise qui débute (arg2) et ses attributs.
		L'argument "liste" peut s'avérer être un objet BeautifulSoup (ex: list(parseur.find(balise, attributs)))
		Cette fonction nettoie des balises "<>" et de leur contenu une liste.
		ex: "<salutation>Bonjour!</salutation>" --> "Bonjour!"
		"""
    return [y for y in [re.sub('<[^<]+?>', '', str(elt)).strip() for elt in liste] if y != ""]


def subprocess_command(commande, stdout=False):
    """
    :param commande: string
    :param stdout: False (par défaut)
    :return: rien si stdout est à False san quoi il retourne une liste.
    """
    if not isinstance(commande, str):
        print("Erreur: ",type(commande))
    else:
        appel = subprocess.Popen(shlex.split(commande), stdout=subprocess.PIPE, universal_newlines=True)
        if stdout == True:
            return [y for y in [element.strip() for element in appel.stdout.readlines()] if y != '']
        fermeture = appel.communicate()
    return


def renommer_fichier(parent):
    """
	Fonction qui prend un chemin vers un dossier, regarde ses composants
	et si ce sont des dossiers il crée "enfants", ensuite en utilisant
	subprocess_command, on renomme avec la commande mv "oldName newName"
	La ligne suivante fait la même action mais sur une seule ligne.
	[[print("mv '{0}' '{1}'".format(parent+"/"+element+"/"+fichier,parent+"/"+element+os.path.splitext(fichier)[1])) for fichier in os.listdir(parent+"/"+element) if (len(os.listdir(parent+"/"+element)) == 1)] for element in enfants]
	"""
    enfants = [enfant for enfant in os.listdir(parent) if os.path.isdir(os.path.join(parent, enfant))]
    for element in enfants:
        nvPath=parent+"/"+element
        for fichier in os.listdir(parent+"/"+element):
            if len(os.listdir(nvPath)) == 1:
                print("mv '{0}' '{1}'".format(nvPath+"/"+fichier,parent+"/"+element+os.path.splitext(fichier)[1]))
                subprocess_command("mv '{0}' '{1}'".format(nvPath+"/"+fichier,nvPath+"/"+element+os.path.splitext(fichier)[1]))
    return



def Ouverture_lien(string):
    try:
        htmlreq = urllib.request.urlopen(string)
    except urllib.error.HTTPError as err:
        print(err.code)
        return False
    return htmlreq

def db_creation(databaseName,donnees):
	with sqlite3.connect(databaseName) as database:
		curseur = database.cursor()
		curseur.execute('CREATE TABLE IF NOT EXISTS Musiques ()')
		curseur.execute('INSERT INTO Musiques VALUES (?,?,?,?,?,?,?)', donnees)
		database.commit()


def Recuperer_base(databaseName):
	with sqlite3.connect(databaseName) as database:
		curseur = database.cursor()
		curseur.execute('SELECT orthographe, phonétique FROM lexique') 
		liste = curseur.fetchall()
		return liste
