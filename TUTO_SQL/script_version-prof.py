#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import du module sys pour les entrées sorties
import sys
# import du module optparse pour la gestion des options / arguments en ligne de commande
from optparse import OptionParser

def process_tagged_line(line, form2occ, formcat2occ):
    # tronçonnage de la ligne en une liste de couples form/cat
    formcatpairs = line.split(' ')
    # pour chaque couple
    for formcatpair in formcatpairs:
        # tronçonnage sur le premier / en partant de la droite
        (form, cat) = formcatpair.rsplit('/',1)

        # on ignore les ponctuations
       # if cat == 'PONCT':
        #     continue

        # si le mot a déjà été rencontré
        if form in form2occ:
            # on incrémente son nb d'occ
            form2occ[form] += 1
            
            # s'il a déjà été rencontré avec cette catégorie
            if cat in formcat2occ[form]:
                # on incrémente le nb d'occ pour le couple form/cat
                formcat2occ[form][cat] += 1
            else:
                # sinon on initialise nb d'occ à 1
                formcat2occ[form][cat] = 1
        # sinon (on rencontre ce mot pour la première fois)
        else:
            form2occ[form] = 1
            formcat2occ[form] = { cat : 1 }

# chaîne de caractères qui sera affichée si l'option -h est précisée, ou si les options passées ne sont pas celles déclarées
usage=u""" Ce programme lit un corpus taggé au format Brown
           (Une phrase par ligne, chaque ligne étant constituée de couples forme/tag 
           séparés par un espace)
         et affiche sur STDOUT les NBFORMS formes les plus fréquentes,
         avec leur nb total d'occurrences, puis les nbs d'occurrences par catégorie

           %prog [options] FICHIER_TAGGE
"""

# --------------------------------
# gestion des options et des arguments
parser=OptionParser(usage=usage)
# déclaration d'une option
parser.add_option("--nbforms",dest="nbforms",default=30,help=u"Nombre de formes fléchies à afficher", metavar="NBFORMS")

# lecture des arguments et des options passés en ligne de commande
(opts,args) = parser.parse_args()
if (len(args) <> 1):
    exit(usage+u'Il manque le fichier taggé')

input_file = args[0]
nbforms = int(opts.nbforms)
# --------------------------------

# ouverture fichier
try:
    input_stream = open(input_file)
except IOError:
    print "Impossible d'ouvrir", input_file
    exit()

# dico : clé=forme, val=nb d'occ
form2occ = {}
# dico de dico : clé1=forme, clé2=cat, val = nb d'occ de cette forme avec cette cat
formcat2occ = {}

line = input_stream.readline()
while line <> '':
    line = line[:-1] # suppression du retour à la ligne
    line = line.strip() # suppression des éventuels espaces initiaux et finaux

    # on réalise tous les traitements nécessaires sur la ligne que l'on vient de lire
    # (on ne fait pas de stockage pour ensuite faire une relecture...)
    process_tagged_line(line, form2occ, formcat2occ)

    # on relit une ligne
    line = input_stream.readline()

# tri des mots par nb d'occurrences décroissant
sorted_forms = sorted(form2occ.keys(), key = lambda x: form2occ[x], reverse=True) 
        

out_encoding = sys.stdout.encoding
if not out_encoding:
    out_encoding = 'utf-8'
#-- Affichage des formes les plus fréquentes
print "Les ",nbforms,u"formes les plus fréquentes, par ordre décroissant de nb d'occurrences\n et leurs catégories également par ordre décroissant".encode(out_encoding)
for form in sorted_forms[:nbforms]:
    # on trie ses catégories par nb d'occ décroissant
    sorted_catoccs = sorted(formcat2occ[form].items(), key= lambda x:x[1], reverse=True) 

    # on construit une chaine avec les couples "cat":"nb occ"
    s = [ x[0]+':'+str(x[1]) for x in sorted_catoccs ]

    # on affiche la forme, son nb total d'occurrence, et les couples cat/nb occ
    print form + "\t\tocc= " + str(form2occ[form]) + "\t( " + ', '.join(s) + " )"

#-- Calcul du taux moyen d'ambiguité sur formes distinctes (= "par type") :
#    nb de couples forme+categorie divisé par nb total de formes distinctes
#  rem : len(formcat2occ[f].keys()) => donne le nb de categories associees à f
#  rem : len(form2occ.keys() => donne le nb de formes distinctes


print(sum( [ len(formcat2occ[f].keys()) for f in formcat2occ.keys() ] ))
ambig_cat_vocab = sum( [ len(formcat2occ[f].keys()) for f in formcat2occ.keys() ] ) / float( len(form2occ.keys()) )

#-- Calcul du taux moyen d'ambiguité sur les occurrences de formes  (= "par token") :
#   numérateur : pour chaque forme f, ayant cf categories et of occurrences, on pondère cf par of (i.e. on ajoute of * cf)
numer = sum( [ form2occ[f]*len(formcat2occ[f].keys()) for f in formcat2occ.keys() ] )
#   dénominateur = somme du nombre d'occurences total de chaque token dans le corpus
denom = sum( form2occ.values() )
ambig_cat_occ = numer / float(denom)

print(form2occ["de"])
#print(formcat2occ)

# ecriture des nb moyens, arrondis à 3 chiffres après la virgule
print u"Nb moyen de catégories par forme distincte:".encode(out_encoding), '{0:.3f}'.format(ambig_cat_vocab)
print u"Nb moyen de catégories par occurrence de forme:".encode(out_encoding), '{0:.3f}'.format(ambig_cat_occ)


    
