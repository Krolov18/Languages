# -*- encoding: utf-8 -*-
__author__ = 'krolev'
from collections import defaultdict
import sqlite3

class Perceptron(object):
    """
        Cette classe Perceptron est une fusion entre celle vue en cours extraite du tp4 et le code du perceptron moyenné
        fourni pour réaliser ce projet.

    """
    def __init__(self, default_label="NOUN"):
        """
            L'initialisation d'une classe Perceptron instancie deux dictionnaires, dont l'un représentera les poids
            du perceptron, l'autre servira en plus des poids à faire la moyenne dans la méthode average_weights

        :param default_label:
        :return:
        """

        self.weights = defaultdict(lambda: defaultdict(float))
        # valeur accumulée de la paire classe/feature
        self._cached = defaultdict(lambda: defaultdict(float))
        # nombre d'occurence déjà rencontrée
        self.n_updates = 0.0
        # label par défaut
        self.def_label = default_label
        # étiquettes de début de séquence
        self.START = ['-START-', '-START2-']
        # étiquettes de fin de séquence
        self.END = ['-END-', '-END2-']

    def __perceptron_update(self, f, l, how_much):
        """
            Action de la mise à jour.
        :param f: feature
        :param l: label
        :param how_much: (dans notre cas 1) mais de manière générale car valeur constante.
        :return:
        """
        self.weights[l][f] += how_much
        self._cached[l][f] += self.n_updates * how_much
        return

    def update(self, true_label, guessed_label, true_features, guessed_features=None):
        """
            Implémentes la règle du perceptron à mettre à jour le vecteur de poids:
        :param true_label: gold label
        :param guessed_label: label prédit
        :param true_features: gold features
        :param guessed_features: features prédits
        :return:
        """
        """
        Implements the perceptron rule to update weight vector:

            w_{t+1} = w_t + phi(true_label, true_features) - phi(guessed_label, guessed_features)

        If `guessed_features` is `None`, the feature vector is assumed
        to be the same for the true and the predicted label.
        """

        self.n_updates += 1

        if true_label == guessed_label:
            return

        if guessed_features is None:
            for f in true_features:
                self.__perceptron_update(f, true_label, +1)
                self.__perceptron_update(f, guessed_label, -1)
        else:
            for f in true_features:
                self.__perceptron_update(f, true_label, +1)
            for f in guessed_features:
                self.__perceptron_update(f, guessed_label, -1)
        return

    def score(self, features, labels=None):
        """
            score calcule la fonction de décision pour chaque label. et renvoie le resultat
            sous forme de dictionnaire (defaultdict).
            Cette fonction peut s'appliquer de manière globale quand labels est à None
            mais elle peut s'appliquer sur un seul label.
        :param features: defaultdict
        :param labels: (default: None) string
        :return: scores
        """

        if labels is None:
            labels = self.weights.keys()

        scores = defaultdict(float)
        for c in labels:
            scores[c] = self.decision_function(features, c)

        return scores

    def predict(self, features, possible_labels=None):
        """
            Prdit le label associé à un vecteur de poids

            Parameters
            ----------
            - features, a dictionnary
                a dictionnary mapping feature names to their value
            - possible_labels, an iterable
                if not None, only the set of possible labels (i.e. the argmax of
                the decision rule) is reduced to this set

        :param features: defaultdict
        :param possible_labels: iterable
        :return: renvoie le label maximisé
        """

        scores = self.score(features)
        if len(scores) == 0:
            return self.def_label

        if possible_labels is not None:
            scores = {k: v for k, v in scores.items() if k in possible_labels}

        return max(scores, key=lambda label: (scores[label], label))

    def normalize(self, word):
        """
            Remplace certains types de tokens par des pseudos-mots

        :param word: string
        :return: string
        """
        if '-' in word and word[0] != '-':
            return '!HYPHEN'
        elif word.isdigit() and len(word) == 4:
            return '!YEAR'
        elif word[0].isdigit():
            return '!DIGITS'
        elif word == "X":
            return "NOUN"
        else:
            return word.lower()

    def train(self, train_data, dev_data, nr_iter):
        """
            Entraîne un perceptron sur le corpus train_data, en réalisant
            nr_iter itérations sur train_data.
            Renvoie les paramètres appris (c'est à dire un vecteur pour chaque catégorie)

        :param train_data: liste de tuples
        :param dev_data: liste de tuples
        :param nr_iter: integer
        :return: None
        """
        import random

        for i in range(nr_iter):
            for words, tags in train_data:
                self.train_one_sentence(words, tags)
            print("Epoch {}  train acc = {}\t dev acc = {}".format(
                i, self.evaluate(train_data), self.evaluate(dev_data)
                )
            )
            random.shuffle(train_data)
        None

    def get_features(self, i, word, context, prev1, prev2):
        """

                Renvoie un dictionnaire de features extraits à partir des tokens de la phrase

        Exemple :
            i           : 4
            word        : dort
            context     : ['-START-', '-START2-', 'le', 'chat', 'dort', '.', '-END-', '-END2-']
            prev        : 'N'
            prev2       : 'D'

        :param i: indice du token dans la liste context
        :param word: token à étiqueter
        :param context: liste de strings
        :param prev1: tag précédent le mot
        :param prev2: tag précédent prev1
        :return: features
        """
        features = defaultdict(float)

        features["bias="]  = 1                   # biais (constant)
        features["wi=" + word] = 1              # forme du mot
        features["form=" + context[i]] = 1      # forme normalisée du mot (éventuellement remplacé par un pseudo-mot  à l'aide de la fonction _normalize
        features["suf-3=" + word[-3:]] = 1       # 3 dernières lettres
        features["pref-2=" + word[:2]] = 1       # 2 premières lettres
        features["wi-1=" + context[i-1]] = 1    # mot précédent
        features["wi-2=" + context[i-2]] = 1    # 2ème mot précédent
        features["wi+1=" + context[i+1]] = 1    # mot suivant
        features["wi+2=" + context[i+2]] = 1    # 2ème mot suivant
        features["ti-1=" + prev1] = 1            # tag précédent
        features["ti-2=" + prev2] = 1           # 2ème tag précédent
        features["ti-1ti-2=" + prev1 + prev2] = 1 # 2 derniers tags (trait bigramme)
        return features

    def train_one_sentence(self, words, tags):
        """
            Entraîne le perceptron sur la phrase représentée par words et tags.

        :param words: liste de mots
        :param tags: liste de tags de la même taille que words
        :return: None
        """
        prev1, prev2 = self.START
        context = self.START + [self.normalize(w) for w in words] + self.END

        for i, word in enumerate(words):
            ind = i+len(self.START)
            features = self.get_features(i+len(self.START), word, context, prev1, prev2)
            guessed_label = self.predict(features)            # on réalise une prédiction
            self.update(tags[i], guessed_label, features)     # mise à jour des poids du perceptron
            prev2, prev1 = prev1, guessed_label
        return

    def tag_one_sentence(self, words):
        """
            Prédit et renvoie une séquence de tags pour la phrase words en utilisant
            les features.

        :param words: liste de string
        :return: liste
        """
        prev1, prev2 = self.START
        context = self.START + [self.normalize(w) for w in words] + self.END

        tags = []

        for i, word in enumerate(words):
            features = self.get_features(i+len(self.START), word, context, prev1, prev2)
            tag = self.predict(features)           # on réalise une prédiction
            tags.append(tag)                       # on ajoute tag predit à tags
            prev2, prev1 = prev1, tag              # on met à jour les prev1 e tprev2
        return tags

    def tag(self, sentences):
        """
            Cette méthode renvoie une liste de couples tuplés (mots, tags_predits)

        :param sentences: liste de tuples
        :return: liste de tuples
        """
        guessed = []
        for words, tags in sentences:
            guessed_tags = self.tag_one_sentence(words)
            assert len(guessed_tags) == len(tags)
            guessed.append((words, guessed_tags))
        return guessed

    def evaluate(self, sentences):
        """
            Prédit les tags de toutes les phrases de sentences puis calcule
            l'exactitude sur les séquences prédites.
            L'exactitude est le nombre de tags corrects divisé par le nombre total de tags

        :param sentences: liste de tuples
        :return: float
        """
        acc = 0.0
        total = 0.0
        for words, tags in sentences:
            guessed_tags = self.tag_one_sentence(words)
            assert len(guessed_tags) == len(tags)
            for i, tag in enumerate(tags):
                if tag == guessed_tags[i]:
                    acc += 1.0
            total += len(words)
        return acc / total

    def decision_function(self, features, label):
        """
            Calcul de la fonction décision

        :param features: dictionnaire
        :param label: string
        :return: float
        """
        return sum(features[f] * self.weights[label][f] for f in features)

    def average_weights(self):
        """
            calcule la moyenne de tous les vecteurs
            de poids sucessifs obtenus.

        :return: None
        """
        t = 1.0 / self.n_updates
        for label in self.weights:
            for f in self.weights[label]:
                self.weights[label][f] -= t * self._cached[label][f]
        return