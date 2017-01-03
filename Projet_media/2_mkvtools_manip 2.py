# -*- coding: UTF-8 -*-
__author__ = "Krolev"

"""
Script Gérant la création ou la manipulation de fichier videos
Création de fichier mkv

Le fichier lu dans download doit être renommer une fois par le user. après c'est bon.

"""
import shlex, subprocess
import re
import urllib.request
import sys, os, glob
import itertools
import codecs
import yaml
try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

def subprocess_command(commande, stdout=False):
	if not isinstance(commande, str):
		print("Erreur: ",type(commande))
	else:
		appel = subprocess.Popen(shlex.split(commande), stdout=subprocess.PIPE, universal_newlines=True)
		if stdout == True:
			return [y for y in [element.strip() for element in appel.stdout.readlines()] if y != '']
		fermeture = appel.communicate()

def grouperElements(liste, function=len):
	lexique=[]
	data=sorted(liste, key=function)
	for k,g in itertools.groupby(data, function):
		lexique.append(list(g))
	return lexique

def verifier_membresListe(liste):
	nvListe = []
	for i in range(1,len(liste)):
		if len(liste[0]) == len(liste[i]):
			nvListe.append(True)
		else:
			nvListe.append(False)
	return all(nvListe)

def rechercher(liste, recherche="language", verite=False):
	for element in liste:
		if recherche in element:
			if verite:
				return True
			else:
				return element


class Creer_MKV:
	def __init__(self):
		self.ffmpegCommande = "ffmpeg -i '{0}' '{2}' '{3}' 'copy' '{1}'"
		self.delCommande = "rm '{0}'"
		self.fileCommande = "'{0}'"
		self.creerCommande = "mkvmerge -o '{0}' {1}"
		self.language = "--language 0:{0}"

	
	def decomposer_flux(entree, sortie, audio=False,video=False):
		if audio:
			commandeExtraireAudio = self.ffmpegCommande.format(entree, sortie, "-vn","-acodec")
			subprocess_command(commandeExtraireAudio)
		if video:
			commandeExtraireVideo = self.ffmpegCommande.format(entree,sortie,"-an","-vcodec")
			subprocess_command(commandeExtraireVideo)
	
	
	def supprimer_inutile(pathFile):
		subprocess_command(self.delCommande.format(nomFichier))
	
	def ajouter_flux2mkv(source, extention, langue, pathFiles):
		files = []
		sortie = ".".join([source+"1",extention])
		for element in pathFiles:
			files.append(self.fileCommande.format(" ".join([element,self.language.format(langue)]))
		subprocess_command(self.creerCommande.format(sortie," ".join(files)))
	
	def reconstruire_flux(sortie, flux):
		files = []
		for flu in flux:
			files.Append(" ".join(self.fileCommande.format(flu[0]),self.language.format(flu[1])))
		subprocess_command(self.creerCommande.format(sortie," ".join(files)))



envoi = input("donnez le type de l'extention (video, audio) ")

def verifier_format(type,extention):
	Formats = yaml.load(open("/home/krolev/Documents/Projet_media/BIBLIOTHEQUES/formats_acceptes.yaml",'r'), Loader=Loader)
	if type == "audio" and not extention in Formats["formats_audio"]:
		Formats["formats_audio"].append(extention)
	elif type == "video" and not extention in Formats["formats_video"]:
		Formats["formats_video"].append(extention)
	with open("/home/krolev/Documents/Projet_media/BIBLIOTHEQUES/formats_acceptes.yaml", "w") as yaml_file:
		yaml_file.write(yaml.dump(Formats))

mkvMerge = 'mkvmerge -I {0}'
(nom,separator,extention) = fichier.rpartition('.')
nomEchappe = nom.replace(' ','\ ')


###Chargement de la partie mkvmerge
lectureMKVmerge = subprocess_command(mkvMerge.format(fichier),True)

metadata=[]
if extention == "mkv":
	for line in lectureMKVmerge:
		if "Track ID" in line:
			temp = line.split()
			type = temp[3]
			ID = temp[2]
			langue = rechercher(temp).split(':')[1][:2]
			if not "video" in line:
				extention = temp[4].strip('()').split('/')[0]
			if 'audio' in line:
				extention = temp[4].strip('()').split('/')[-1]
			if 'subtitles' in line:
				extention = temp[4].strip('()').split('/')[-1]
			metadata.append((type,ID,language,extention))
if extention not in ["mkv","srt"]:
	for line in lectureMKVmerge:
		print(line)
		


temp = grouperElements(metadata,function=lambda liste: liste[2]) # tri par langue
print(temp)
for element in temp:
	if not rechercher(element, "subtitles",verite=True) and rechercher(element, "audio",verite=True):
		subprocess_command("periscope -l '{0}' '{1}'".format(element[0][2],fichier))

