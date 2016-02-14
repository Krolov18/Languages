# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from codecs import open
from collections import defaultdict

__author__ = 'Ko-Mél-Clé-Thim'

class ConfusionMatrix(object):
    def __init__(self, guessed_sentences, gold_sentences):
        """
        construit et renvoie une matrice de confusion
        on suppose les phrases données dans le même ordre
        """
        self.matrix = defaultdict(lambda : defaultdict(int))
        assert len(guessed_sentences) == len(gold_sentences)
        for i, sentence in enumerate(gold_sentences):
            or_tags = sentence[1]
            perc_tags = guessed_sentences[i][1]
            for j, tag in enumerate(or_tags):
                self.matrix[perc_tags[j]][or_tags[j]] += 1

    def getMatrice(self):
        return self.matrix

    def __str__(self):
        """
        format str pour une matrice de confusion
        """
        sep = " | "
        padding = max([len(k) for k in self.matrix.keys()])
        _str = (" "*padding)+ sep + sep.join([key + ((padding - len(key)) * " ") for key in self.matrix.keys()]) + sep
        for key in self.matrix.keys():
            _str += '\n' + key + ((padding - len(key))*" ")+ sep
            for key2 in self.matrix.keys():
                _str += str(self.matrix[key][key2]) + str((padding - len(str(self.matrix[key][key2])))*" ") + sep
        return _str

    def confused_classes(self, threshold=0.9):
        """
        renvoie une liste de tuples (tag1, [tag2...])
        telle que tag1 est souvent mal classe comme tag2
             - matrix est matrice de confusion
             - threshold donne le pourcentage minimal
        d'instances bien classees
        """
        assert threshold < 1
        l = []
        candidates = []
        for keyt in self.matrix.keys():
            total = sum([self.matrix[k][keyt] for k in self.matrix.keys()])
            num_thresh = total * threshold
            if num_thresh >= self.matrix[keyt][keyt]:
                candidates = list(filter(lambda k:  self.matrix[keyt][k] > total - num_thresh or self.matrix[k][keyt] > total - num_thresh, self.matrix.keys()))
                if len(candidates) == 0:
                    candidates = self.matrix.keys()
                candidates = filter(lambda k:  k != keyt and (self.matrix[keyt][k] != 0 or self.matrix[k][keyt] != 0), self.matrix.keys())
                candidates = map(lambda c: str(c), candidates)
                candidates = sorted(candidates, key=lambda k: abs(self.matrix[keyt][k] - self.matrix[k][keyt]), reverse=True)
            if (len(candidates) != 0) : l.append((str(keyt), candidates))
            candidates = []
        return l