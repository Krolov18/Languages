# -*- encoding: utf-8 -*-
from __future__ import division, print_function, unicode_literals, with_statement
from dependency_parser import *
from codecs import open
import random
import yaml
from read_conll_data import *


################################
#
# Pour lancer les lignes de la condition "__main__", 
# il suffit de commenter/decommenter
# les différentes instances dde l'analyseur.
# Il y a trois instances soit trois blocs.
#
#
#
################################





if __name__ == "__main__":
    # Récupération des données
    (train_data, dev_data, test_data) = get_universal_treebank_data("de")
    guessed_data = yaml.load(open("deutsch_univTagSet2.yaml"))
    train_data = list(filter(lambda s: check_projectivity(s[2]), train_data))   # garder uniquement les arbres projectifs
    # Taille des donées (en nombre de phrases)
    print("Train dataset : {} sentences".format(len(train_data)))
    print("Dev dataset   : {} sentences".format(len(dev_data)))
    print("Test dataset  : {} sentences".format(len(test_data)))
    parser = ArcHybridParser(dp_features) # ArcHybrid Parsing algorithm
    print("Training ...")
    train_dependency_parser(parser, guessed_data, dev_data, 5)            # entraînement, 5 : nombre d'itérations sur les données (typiquement entre 5 et 20)
    print("UAS on test : ", test_dependency_parser(parser, test_data))  # test parser on test dataset

    # Récupération des données
    (train_data, dev_data, test_data) = get_universal_treebank_data("fr")
    guessed_data = yaml.load(open("french_univTagSet2.yaml"))
    train_data = list(filter(lambda s: check_projectivity(s[2]), train_data))   # garder uniquement les arbres projectifs
    # Taille des donées (en nombre de phrases)
    print("Train dataset : {} sentences".format(len(train_data)))
    print("Dev dataset   : {} sentences".format(len(dev_data)))
    print("Test dataset  : {} sentences".format(len(test_data)))
    parser = ArcHybridParser(dp_features) # ArcHybrid Parsing algorithm
    print("Training ...")
    train_dependency_parser(parser, guessed_data, dev_data, 5)            # entraînement, 5 : nombre d'itérations sur les données (typiquement entre 5 et 20)
    print("UAS on test : ", test_dependency_parser(parser, test_data))  # test parser on test dataset

    # Récupération des données
    (train_data, dev_data, test_data) = get_tiger_corpus_data()
    guessed_data = yaml.load(open("tiger_corpus_richTagSet2.yaml"))
    train_data = list(filter(lambda s: check_projectivity(s[2]), train_data))   # garder uniquement les arbres projectifs
    # Taille des donées (en nombre de phrases)
    print("Train dataset : {} sentences".format(len(train_data)))
    print("Dev dataset   : {} sentences".format(len(dev_data)))
    print("Test dataset  : {} sentences".format(len(test_data)))
    parser = ArcHybridParser(dp_features) # ArcHybrid Parsing algorithm
    print("Training ...")
    train_dependency_parser(parser, guessed_data, dev_data, 5)            # entraînement, 5 : nombre d'itérations sur les données (typiquement entre 5 et 20)
    print("UAS on test : ", test_dependency_parser(parser, test_data))  # test parser on test dataset
