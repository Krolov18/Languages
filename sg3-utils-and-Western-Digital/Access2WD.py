# -*- coding: UTF-8 -*-

from subprocess import Popen, PIPE
import re
import shlex
import re
import getpass
import os

##Décommentez la ligne suivante et remplcer ce qu'il y a entre <> par le chemin du dossier wdpassport-utils

#path=<emplacement du dossier wdpassport-utils>
#Exemple: path='/media/USER/Documents/wdpassport-utils'

for file in os.listdir(path):
	if file != 'usbrest':
		appelCompilation=shlex.split('gcc usbreset.c -o usbreset')
		compilation=Popen(appelCompilation,stdout=PIPE)
		arretCompilation=compilation.communicate()

##Attention avec l'opération suivante. Il se peut qu'en faisant "./cookpw.py", l'ordinateur vous renvoie ./cookpw.py: command not found
##la raison est que le fichier de doit pas avoir les droits que vous lui demander.
##Il suffit alors avant de lancer ce script de lancer manuellement dans le terminal les deux commandes suivantes:
##-- ls -l
##-- chmod a+rwx cookpw.py --> cela vet dire je donne l'autorisation à tous (a=all) les users d'utiliser ce fichier avec
##   les trois types r pour read, w pour write et x pour execute. commande uniquement appliquée au fichier cookpw.py


	elif file != 'password.bin':
##remplacer ce qu'il y a entre <> par votre mot de passe
		appelCompilation=shlex.split('./cookpw.py <MotDePasse> > password.bin')
		compilation
		arretCompilation


##Ces deux premières lignes de codes suivantes nous permettent d'avoir accès à la ligne que matche grep.

rechercheSGnum=Popen("dmesg | grep sg | grep 'type 13'",  shell=True, stdout=PIPE,universal_newlines=True)
lectureSGnum=rechercheSGnum.stdout.readlines()

##Ces deux lignes suivantes vont nous permettent d'avoir accès à la liste des composants usb attachés à l'ordinateur.

appelWD = Popen('lsusb', stdout=PIPE)
lectureWD = appelWD.stdout.readlines()

##Cette première boucle va chercher le numéro du SG grâce au module re. puis une fois matché, ce numéro
##est stocké dans une variable qui nous servira dans la seconde boucle

sgNumliste=[]
for ligne in lectureSGnum:
	ligne=re.sub('\n','',ligne)
	searchSGnum=re.search('(sg)([1-9])',ligne)
	if searchSGnum:
		k=searchSGnum.group(2)
		if k not in sgNumliste:
			sgNumliste.append(k)
			SGnum=str(sgNumliste)[1:-1]

##Dans cette seconde boucle nous accèdons au contenu de "lectureWD"

for ligne in lectureWD:
	ligne=ligne.decode('utf-8')
	if 'Western Digital Technologies' in ligne:
		recherche=re.findall('[0-9]{3}',ligne) ##cela génère une liste
		if recherche:
			print(recherche)
			sudoPassword=getpass.getpass()
			commandeOuverture='sg_raw -s 40 -i password.bin /dev/sg%s c1 e1 00 00 00 00 00 00 28 00' % (SGnum)
			commandeReboot='./usbreset /dev/bus/usb/%s/%s' %(recherche[0],recherche[1]) ## nous n'avons besoin que des deux premiers éléments de la liste
			appelOuverture=Popen('echo %s|sudo -S %s' % (sudoPassword, commandeOuverture),stdout=PIPE,shell=True)
			ArretsubOuverture=appelOuverture.communicate()
			appelReboot=Popen('echo %s|sudo -S %s' %(sudoPassword,commandeReboot),stdout=PIPE,shell=True)
			ArretsubReboot=appelReboot.communicate()
