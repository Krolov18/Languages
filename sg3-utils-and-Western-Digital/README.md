sg3-utils-and-Western-Digital
=============================

open a WD drive disc in linux

Il faut avoir installer le paquet sg3-utils, il suffit de taper dans un terminal l commande suivante:

<code>sudo apt-get install sg3-utils</code>

Ensuite on fait une copie du dossier de KenMacD à l'emplacement de son choix sur l'ordinateur puis on lance cette commande:

<code>git clone https://github.com/KenMacD/wdpassport-utils.git</code>

Cela crée donc un dossier wdpassport-utils.
En lisant le README dans ce dossier, il nous est demandé de générer le mot de passe ainsi que de
compiler le programme écrit en c (usbreset.c).
Le script python que j'ai écrit fait cela pour vous. Vous n'avez simplement qu'à lancer le script python.

<code>python3 AccessWD.py</code>
