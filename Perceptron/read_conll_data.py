# -*- encoding: utf-8 -*-
import codecs
import random
__author__ = 'krolev'


def read_conll_tagging_data(filenam, max_sent=None):
    """
    Lit un corpus au format conll et renvoie une liste de couples.
    Chaque couple contient deux listes de même longueur :
        la première contient les mots d'une phrase
        la seconde contient les tags correspondant
    Par exemple :

        [(["le", "chat", "dort"],["DET", "NOUN", "VERB"]),
          (["il", "mange", "."],["PRON", "VERB", "."]),
         ...etc
         ]

    """
    with codecs.open(filename=filenam, mode="r", encoding="utf-8") as inStream:
        count = 0
        loc = inStream.read()
        sentences = []
        for sent_str in loc.strip().split('\n\n'):
            if max_sent is not None and max_sent < count:
                break
            count += 1
            lines = [line.split() for line in sent_str.split('\n')]
            words = []
            tags = []
            for _, word, _, coarse_pos, _, _, _, _, _, _ in lines:
                words.append(word)
                tags.append(coarse_pos)
            sentences.append((words, tags))
        return sentences

def get_tiger_corpus_data() :
    """
    Fonction pour lire les corpus d'entraînement, de développement et de
    test du tiger corpus (voir lien sur didel).
    """
    trainset = "./data/german/tiger/train/german_tiger_train_copie.conll"
    testset  = "./data/german/tiger/test/german_tiger_test_copie.conll"
    train_data = read_conll_tagging_data(trainset)
    random.shuffle(train_data)
    split = len(train_data) // 20   # on garde 5% du corpus d'entraînement pour servir de corpus de développement)
    dev_data,train_data = train_data[:split], train_data[split:]
    test_data  = read_conll_tagging_data(testset)

    return (train_data, dev_data, test_data)

def get_universal_treebank_data(language):
    """
    Fonction pour lire les corpus d'entraînement, de développement et de test pour la langue language
    ("fr" pour français, "de" pour allemand, etc -> voir les données)
    """
    trainset = "./universal_treebanks_v2.0/std/{0}/{0}-universal-train.conll".format(language)
    devset = "./universal_treebanks_v2.0/std/{0}/{0}-universal-dev.conll".format(language)
    testset = "./universal_treebanks_v2.0/std/{0}/{0}-universal-test.conll".format(language)
    train_data = read_conll_tagging_data(trainset)
    dev_data = read_conll_tagging_data(devset)
    test_data = read_conll_tagging_data(testset)
    return (train_data, dev_data, test_data)
