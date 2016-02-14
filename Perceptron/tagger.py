# -*- encoding: utf-8 -*-
__author__ = 'krolev'

from read_conll_data import *
# from Perceptron import Perceptron
from Perceptron3 import Perceptron3
from codecs import open
from matrice_confusion import ConfusionMatrix
import yaml
import codecs
from read_conll_data import *

def TaggingCorpora(language="de", universal=False, outputName="sortie.yaml"):
    """

    Cette fonction est juste un raccourci. Elle taggue, et enregistre
    les guessed_sentences dans un ficheir au format yaml afin
    d'utiliser l'output comme input de la matrice de confusion.
    Les parties commentés sont les conditions utilisées pour
    regrouper les classes au sein de chauqe corpus.

    :param language: string indiquant la langue du corpus
    :param universal: booléen permettant de prende des données universelles ou fines
    :param outputName: un nom de fichier de sortie
    :return: None
    """
    perceptron = Perceptron3()
    if universal:
        (train_data, dev_data, test_data) = get_universal_treebank_data(language)
        ## Le bloc commenté si dessous représente les fusions apportées au corpus d'entrainement
        # if language == "fr":
        #     for i in range(len(train_data)):
        #         for k in range(len(train_data[i][1])):
        #             if train_data[i][1][k]=="X":
        #                 train_data[i][1][k]="NOUN"
    else:
        (train_data, dev_data, test_data) = get_tiger_corpus_data()
        ## Le bloc commenté si dessous représente les fusions apportées au corpus d'entrainement
        # for i in range(len(train_data)):
        #     for k in range(len(train_data[i][1])):
        #         if train_data[i][1][k]=="PTKANT":
        #             train_data[i][1][k]="PROAV"
        #         elif train_data[i][1][k]=="VVIMP":
        #             train_data[i][1][k]="NE"
        #         elif train_data[i][1][k]=="PTKA":
        #             train_data[i][1][k]="APPR"
        #         elif train_data[i][1][k]=="FM":
        #             train_data[i][1][k]="NE"
        #         if train_data[i][1][k]=="XY":
        #             train_data[i][1][k]="NE"
    perceptron.train(train_data, dev_data, 10)
    perceptron.average_weights()
    print("Résultats sur le corpus de test : {0}".format(perceptron.evaluate(test_data)))
    datas = perceptron.tag(test_data)
    yaml.dump(datas, open(outputName, 'w', 'utf-8'), allow_unicode=True, default_flow_style=False)



################################
#
# Pour lancer les lignes du Main il suffit de commenter/decommenter
# les différentes instances du Perceptron.
# Il y a trois instances soit trois blocs.
#
#
#
################################



if __name__ == '__main__':
    # Tagging du conll deutsch (universal tagset) :
    ## Entrainement sur corpus
    TaggingCorpora(language="de", universal=True, outputName="deutsch_univTagSet3.yaml")
    ## Regard sur la matrice de confusion
    with codecs.open("deutsch_univTagSet3.yaml","r","utf-8") as fichier:
        guessed_data = yaml.load(fichier)
    (train_data, dev_data, test_data) = get_universal_treebank_data("de")
    matriceConfusion = ConfusionMatrix(guessed_data,test_data)
    ### str(matriceConfusion) affiche l'état de la matrice
    with codecs.open("deutsch_univTagSet3.csv","w","utf-8") as sortiee:
        sortiee.write(str(matriceConfusion))
    print()
    ### la méthode_confused_classes() permet avec un
    ### seuil de tolérance, d'afficher les éléments potentiellement fusionnables
    for element in matriceConfusion.confused_classes():
        print(element)

    # Tagging du conll french (universal tagset) :
    ## Entrainement sur corpus
    TaggingCorpora(language="fr", universal=True, outputName="french_univTagSet3.yaml")
    ## Regard sur la matrice de confusion
    with codecs.open("french_univTagSet3.yaml","r","utf-8") as fichier:
       guessed_data = yaml.load(fichier)
    (train_data, dev_data, test_data) = get_universal_treebank_data("fr")
    matriceConfusion = ConfusionMatrix(guessed_data,test_data)
    ### str(matriceConfusion) affiche l'état de la matrice
    with codecs.open("french_univTagSet3.csv","w","utf-8") as sortiee:
        sortiee.write(str(matriceConfusion))
    print()
    ### la méthode_confused_classes() permet avec un
    ### seuil de tolérance, d'afficher les éléments potentiellement fusionnables
    for element in matriceConfusion.confused_classes():
       print(element)

    # tagging du tiger corpus avec etiquettes riches :
    ## Entrainement sur corpus
    TaggingCorpora(outputName="tiger_corpus_richTagSet2.yaml")
    with codecs.open("tiger_corpus_richTagSet2.yaml","r","utf-8") as fichier:
        guessed_data = yaml.load(fichier)
    (train_data, dev_data, test_data) = get_tiger_corpus_data()
    matriceConfusion = ConfusionMatrix(guessed_data, test_data)
    ### str(matriceConfusion) affiche l'état de la matrice$
    with codecs.open("tiger_corpus_richTagSet2.matrix","w","utf-8") as sortiee:
        sortiee.write(str(matriceConfusion))
    print()
    ### la méthode_confused_classes() permet avec un
    ### seuil de tolérance, d'afficher les éléments potentiellement fusionnables
    for element in matriceConfusion.confused_classes():
        print(element)
