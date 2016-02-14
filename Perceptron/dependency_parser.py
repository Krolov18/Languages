# encoding: utf8
# Copyright (c) 2013-2014 Matthew Honnibal, Guillaume Wisniewski, Oana
# Jean-Marie

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""A concise implementation of an arc-hybrid and arc-eager dependency
parser.

Based on the implementation of Matthew Honnibal.
(http://honnibal.wordpress.com/2013/12/18/a-simple-fast-algorithm-for-natural-language-dependency-parsing/)

"""

from __future__ import division, print_function, unicode_literals, with_statement

import abc
import sys
import random
import logging

from collections import defaultdict

## added
from copy import deepcopy as copy
from Perceptron import *
from six import with_metaclass


SHIFT = 0
RIGHT = 1
LEFT = 2
REDUCE = 3
ARC_HYBRID_MOVES = (SHIFT, RIGHT, LEFT)
ARC_EAGER_MOVES = (SHIFT, RIGHT, LEFT, REDUCE)
START = ['-START-', '-START2-']
END = ['-END-', '-END2-']

logging.basicConfig(level=logging.DEBUG)


class DefaultList(list):

    def __init__(self, what=[], default=None):
        self.default = default
        list.__init__(self, what)

    """
    A list that returns a default value if index out of bounds.
    """
    def __getitem__(self, index):
        try:
            return list.__getitem__(self, index)
        except IndexError:
            return None


class Parse:

    def __init__(self, n):
        self.n = n
        self.heads = [None] * (n - 1)
        self.lefts = [DefaultList(default=0) for _ in range(n + 1)]
        self.rights = [DefaultList(default=0) for _ in range(n + 1)]

    def add(self, head, child):
        self.heads[child] = head
        if child < head:
            self.lefts[head].append(child)
        else:
            self.rights[head].append(child)

    def __str__(self):
        return "\n".join(["n={}".format(self.n),
                          "heads={}".format(self.heads),
                          "lefts={}".format(self.lefts),
                          "rights={}".format(self.rights)])


class AbstractParser(with_metaclass(abc.ABCMeta, object)) : 

    """An abstract dependency parser that implements a
    transition-based strategy (either arc-hybrid or arc-eager).

    The parser can only predict the dependency tree structure and not
    the label of the different edges.

    """

    def __init__(self, feature_template, moves, tagger=None):
        """
        Parameters
        ----------
        - feature_template, a callable
             the method to extract features for the dependency parser
        """
        self.moves = moves
        self.model = Perceptron(self.moves)
        self.tagger = tagger
        self.extract_features = feature_template

    def parse(self, words, pos_tags=None):
        """
        Predict the dependencies of a sentence

        Parameters
        ----------
        - words, a sequence of strings
                the (tokenized) sentence
        - tags, a sequence of strings or None
                POS tags of the sentence; if no POS tags are given,
                POS are automatically predicted.
        """
        for _, _, _, parse in self._infer(words, None, pos_tags):
            pass

        return None, parse.heads

    def train_online(self, words, gold_heads, pos_tags=None):
        """
        Online training of the dependency parser with one sentence

        The training procedure infere the dependency tree of a
        sentence and update the weight vector each time a decision is
        made.

        Parameters
        ----------

        - words, a sequence of strings
            the words of the sentence
        - gold_heads, a sequence of integers
            the gold dependency tree
        """

        for guess, best, features, parse in self._infer(words, gold_heads, pos_tags):
            self.model.update(best, guess, features)

        n = len(words)
        return len([i for i in range(n - 1)
                    if parse.heads[i] == gold_heads[i]])

    def _infer(self, words, gold_heads=None, pos_tags=None):
        """Apply the current policy to build the dependency tree of the
        given word sequence.

        Parameters
        ----------

        - words, a list of strings
            the (tokenized) sxsentence
        - gold_heads, a list of integers
            the gold heads. If `None`, the best move at each position
            is also computed.
        - pos_tags, a list of strings
            the PoS tags of the sentence. If `None`, the PoS tags are
            automatically predicted
        """

        n = len(words)
        # Description of the state of the parser
        # --------------------------------------
        #
        # Index describing where we are in the input sentence. This
        # index allows us to access to the “buffer” used in the
        # dependency litterature (buffer = sentence[idx:])
        idx = 2
        # Words that that occurs before idx but for which we have not
        # predict a head yet (--> partially processed words)
        stack = [1]
        # Structure to hold the partially predicted tree
        parse = Parse(n)
        # the decisions we made
        history = []

        if pos_tags is None:
            assert self.tagger is not None, "pos_tags can not be set to None"
            pos_tags = self.tagger.tag(words)

        while stack or (idx + 1) < n:
            features = self.extract_features(words, pos_tags, idx, stack, parse, history)
            scores = self.model.score(features)

            valid_moves = self.get_valid_moves(idx, n, stack, parse.heads)
            guess = max(valid_moves, key=lambda move: scores[move])

            history.append(guess)

            if gold_heads is not None:
                gold_moves = self.get_gold_moves(idx, n, stack, parse.heads, gold_heads)
                # gold_moves is empty iif the tree is not projective
                assert gold_moves
                best = max(gold_moves, key=lambda move: scores[move])
            else:
                best = None

            yield guess, best, features, parse

            idx = self.transition(guess, idx, stack, parse)

    @abc.abstractmethod
    def transition(self, move, i, stack, parse):
        """
        Make the action `move` by modifying the buffer (i.e. the
        position in the sentence `i`), the `stack` and updating the
        (partial) dependency tree accordingly.
        """
        pass

    @abc.abstractmethod
    def get_valid_moves(self, i, n, stack, heads):
        """
        Returns the authorized moves
        """
        pass

    @abc.abstractmethod
    def get_gold_moves(self, n0, n, stack, heads, gold):
        pass


class ArcEagerParser(AbstractParser):

    def __init__(self, features):
        #super().__init__(features, ARC_EAGER_MOVES)
        AbstractParser.__init__(self, features, ARC_EAGER_MOVES)

    def transition(self, move, i, stack, parse):
        if move == SHIFT:
            stack.append(i)
            return i + 1
        elif move == RIGHT:
            parse.add(stack[-1], i)
            stack.append(i)
            return i + 1
        elif move == LEFT:
            parse.add(i, stack.pop())
            return i
        elif move == REDUCE:
            stack.pop()
            return i
        assert move in ARC_EAGER_MOVES

    def get_valid_moves(self, i, n, stack, heads):
        stack_depth = len(stack)
        moves = []
        if i + 1 < n:
            moves.append(SHIFT)
        if stack_depth >= 1 and i + 1 < n:
            moves.append(RIGHT)
        if stack_depth >= 1 and heads[stack[-1]] is None:
            moves.append(LEFT)
        if stack_depth >= 1 and heads[stack[-1]] is not None:
            moves.append(REDUCE)
        return moves

    def get_gold_moves(self, n0, n, stack, heads, gold):
        gold_moves = []
        valid_moves = self.get_valid_moves(n0, n, stack, heads)
        for move in valid_moves:
            if self.get_cost(move, n0, n, stack, heads, gold) == 0:
                gold_moves.append(move)
        return gold_moves

    def get_cost(self, move, n0, n, stack, heads, gold):
        cost = 0
        if move == LEFT:
            for word in range(n0+1, n-1):
                if gold[word] == stack[-1] or gold[stack[-1]] == word:
                    cost += 1
            if n0 != n - 1 and gold[stack[-1]] == n - 1:
                cost += 1
            if n0 != n - 1 and gold[n0] == stack[-1]:
                cost += 1
        if move == RIGHT:
            for word in range(n0 + 1, n):
                if gold[n0] == word:
                    cost += 1
            for word in stack[0:-1]:
                if gold[n0] == word:
                    cost += 1
                if gold[word] == n0 and heads[word] is None:
                    cost += 1
        if move == SHIFT:
            for word in stack:
                if (gold[word] == n0 and heads[word] is None) or gold[n0] == word:
                    cost += 1
        if move == REDUCE:
            for word in range(n0, n-1):
                if gold[word] == stack[-1]:
                    cost += 1
        return cost


class ArcHybridParser(AbstractParser):

    def __init__(self, features):
        #super().__init__(features, ARC_HYBRID_MOVES)
        AbstractParser.__init__(self, features, ARC_HYBRID_MOVES)

    def transition(self, move, i, stack, parse):
        if move == SHIFT:
            stack.append(i)
            return i + 1
        elif move == RIGHT:
            parse.add(stack[-2], stack.pop())
            return i
        elif move == LEFT:
            parse.add(i, stack.pop())
            return i
        assert move in ARC_HYBRID_MOVES

    def get_valid_moves(self, i, n, stack, heads):
        stack_depth = len(stack)
        moves = []
        if i + 1 < n:
            moves.append(SHIFT)
        if stack_depth >= 2:
            moves.append(RIGHT)
        if stack_depth >= 1:
            moves.append(LEFT)
        return moves

    def get_gold_moves(self, n0, n, stack, heads, gold):
        def deps_between(target, others, gold):
            for word in others:
                if gold[word] == target or gold[target] == word:
                    return True
            return False

        valid = self.get_valid_moves(n0, n, stack, heads)
        if not stack or (SHIFT in valid and gold[n0] == stack[-1]):
            return [SHIFT]
        if gold[stack[-1]] == n0:
            return [LEFT]
        costly = set([m for m in self.moves if m not in valid])
        # If the word behind s0 is its gold head, Left is incorrect
        if len(stack) >= 2 and gold[stack[-1]] == stack[-2]:
            costly.add(LEFT)
        # If there are any dependencies between n0 and the stack,
        # pushing n0 will lose them.
        if SHIFT not in costly and deps_between(n0, stack, gold):
            costly.add(SHIFT)
        # If there are any dependencies between s0 and the buffer, popping
        # s0 will lose them.
        # XXX why list?
        if deps_between(stack[-1], list(range(n0+1, n-1)), gold):
            costly.add(LEFT)
            costly.add(RIGHT)
        return [m for m in ARC_HYBRID_MOVES if m not in costly]


# Helper Methods for features extraction
# ======================================

def _get_stack_context(stack, s):
    n = len(stack)
    return tuple(s[stack[-i]] if i - 1 < n else None for i in [1, 2, 3])


def _get_buffer_context(idx, lst):
    d = (lst[idx + i] if i + idx < len(lst) else None for i in [0, 1, 2])
    return tuple(d)


def _get_parse_context(word, deps, data):
    if word == -1:
        return 0, None, None

    deps = deps[word]
    valency = len(deps)
    leftmost = data[deps[-1]] if valency >= 1 else None
    second_leftmost = data[deps[-2]] if valency >= 2 else None

    return valency, leftmost, second_leftmost


def dp_features(words, features, n0, stack, parse, history, delexicalized=False):
    """Extract POS features for dependency parsing

    The feature templates of [Zhang and Nivre, 2011] are used.

    [Zhang and Nivre, 2011] Transition-based Dependency Parsing
    with Rich Non-local Features, ACL'11

    Parameters
    ----------
    - words, a list of strings
         the input sentence.
    - tags, a dictionnary of lists
         features describing the words. Keys correspond to features
         names; values are sequences of string, the i-th string beging
         the feature value for the i-th word.
    - n0, an int
         the word we are extracting features for
    - stack
    - parse, a instance of `Parse`
         the partial parse tree
    - delexicalized, a boolean
         If true, o features describing words are considered so that a
         parser trained on one language can be applied on another
         language (cf. [McDonald et al, 2011]).

    """
    def add(name, *args):
        if delexicalized and "w" in name:
            return # continue

        features[name.format(*args)] = 1
    
    tags = features["fpos"]
    features = defaultdict(int)

    # The name of all features follows the pattern:
    # - a letter: s --> stack n --> buffer
    # - an integer: the position on the stack or on the buffer
    # - an optionnal letter: l = left most child, r = rightmost child
    #   or h for the head
    # - a letter: p for POS tags; w for word identity, v for valency

    s0w, _, _ = _get_stack_context(stack, words)
    s0p, _, _ = _get_stack_context(stack, tags)

    n0w, n1w, n2w = _get_buffer_context(n0, words)
    n0p, n1p, n2p = _get_buffer_context(n0, tags)

    n0lv, n0lp, _ = _get_parse_context(n0, parse.lefts, tags)

    _, n0rp, _ = _get_parse_context(n0, parse.rights, tags)
    _, n0rw, _ = _get_parse_context(n0, parse.rights, words)

    s0lv, s0lp, s0l2p = _get_parse_context(stack[-1], parse.lefts, tags) if len(stack) != 0 else (0, None, None)
    _, s0lw, s0l2w = _get_parse_context(stack[-1], parse.lefts, words) if len(stack) != 0 else (0, None, None)

    s0rv, s0rp, s0r2p = _get_parse_context(stack[-1], parse.rights, tags) if len(stack) != 0 else (0, None, None)
    _, s0rw, s0r2p = _get_parse_context(stack[-1], parse.rights, words) if len(stack) != 0 else (0, None, None)

    head = parse.heads[stack[-1]] if len(stack) != 0 else None
    s0hp = tags[head] if head is not None else None
    s0hw = words[head] if head is not None else None

    # distance between s0 and n0
    # the distance is clipped to 5
    dist = min((n0 - stack[-1], 5)) if len(stack) != 0 else 0

    # Baseline feature template from [Zhang and Nivre, 2011]
    # ======================================================

    # biais
    add("biais", "biais")

    # Single word features
    #
    # S0w/p
    add("s0w/p={}/{}", s0w, s0p)
    # S0w
    add("s0w={}", s0w)
    # S0p
    add("s0p={}", s0p)
    # N0wp
    add("n0w/p={}/{}", n0w, n0p)
    # N0w
    add("n0w={}", n0w)
    # N0p
    add("n0p={}", n0p)
    # N1wp
    add("n1w/p={}/{}", n1w, n1p)
    # N1w
    add("n1w={}", n1w)
    # N1p
    add("n1p={}", n1p)
    # N2wp
    add("n2w/p={}/{}", n2w, n2p)
    # N2w
    add("n2w={}", n2w)
    # N2p
    add("n2p={}", n2p)

    # Word pair features
    #
    # S0wpN0wp
    add("s0wp={}/{}_and_n0wp={}/{}", s0w, s0p, n0w, n0p)
    # S0wpN0w
    add("s0wp={}/{}_and_n0w={}", s0w, s0p, n0w)
    # S0wN0wp
    add("s0w={}_and_n0wp={}/{}", s0w, n0w, n0p)
    # S0wpN0p
    add("s0wp={}/{}_and_n0p={}", s0w, s0p, n0p)
    # S0pN0wp
    add("s0p={}_and_n0wp={}/{}", s0p, n0w, n0p)
    # S0wN0w
    add("s0w={}_and_n0w={}", s0w, n0w)
    # S0pN0p
    add("s0p={}_and_n0p={}", s0p, n0p)
    # N0pN1p
    add("n0p={}_and_n1p={}", n0p, n1p)

    # from three words
    #
    # N0pN1pN2p
    add("n0p={}_and_n1p={}_and_n2p={}".format(n0p, n1p, n2p))
    # S0pN0pN1p
    add("s0p={}_and_n0p={}_and_n1p={}".format(s0p, n0p, n1p))
    # S0hpS0pN0p
    add("s0hp={}_and_s0p={}_and_n0p={}".format(s0hp, s0p, n0p))
    # S0pS0lpN0p
    add("s0p={}_and_s0lp={}_and_n0p={}".format(s0p, s0lp, n0p))
    # S0pS0rpN0p
    add("s0p={}_and_s0rp={}_and_n0p={}".format(s0p, s0rp, n0p))
    # S0pN0pN0lp
    add("s0p={}_and_n0p={}_and_n0lp={}".format(s0p, n0p, n0lp))

    # New features templates
    # ======================
    #
    # distance
    # S0wd
    add("s0w/d={}/{}", s0w, dist)
    # S0pd
    add("s0p/d={}/{}", s0p, dist)
    # N0wd
    add("n0w/d={}/{}", n0w, dist)
    # N0pd
    add("n0pd={}/{}", n0p, dist)
    # S0wN0wd
    add("s0wN0wd={}/{}/{}", s0w, n0w, dist)
    # S0pN0pd
    add("s0pN0pd={}/{}/{}", s0p, n0p, dist)

    # Valency
    # S0wv_r
    add("s0w={}_and_rv={}", s0w, s0rv)
    # S0pv_r
    add("s0p={}_and_rv={}", s0p, s0rv)
    # S0wv_l
    add("s0w={}_and_lv={}", s0w, s0lv)
    # S0pv_l
    add("s0p={}_and_lv={}", s0p, s0lv)
    # N0wv_l
    add("n0p={}_and_lv={}", n0w, n0lv)
    # N0pv_l
    add("n0p={}_and_lv={}", n0p, n0lv)

    # Unigrams
    # S0hw
    add("s0hw={}", s0hw)
    # S0hp
    add("s0hp={}", s0hp)
    # S0lw
    add("s0lw={}", s0lw)
    # S0lp
    add("s0lp={}", s0lp)
    # S0rw
    add("s0rw={}", s0rw)
    # S0rp
    add("s0rp={}", s0rp)
    # N0rw
    add("n0rw={}", n0rw)
    # N0rp
    add("n0rp={}", n0rp)

    # Third-order features
    # S0h2w
#    add("s0h2w={}", s0h2w)
    # s0h2p
#    add("s0h2p={}", s0h2p)
    # s0l2w
    add("s0l2w={}", s0l2w)
    # s0l2p
    add("s0l2p={}", s0l2p)
    # s0r2w
#    add("s0r2w={}", s0r2w)
    # s0r2p
    add("s0r2p={}", s0r2p)
    # n0l2w
    add("s0l2w={}", s0l2w)
    # n0l2p
    # S0pS0lpS0l2p
    # S0pS0rpS0r2p
    # S0pS0hpS0h2p
    # N0pN0lpN0l2p

    # History of decisions
    hist_feat = [history[-i] if i <= len(history) else None for i in range(1, 9)]
    for i, v in enumerate(hist_feat):
        add("hist@-{}={}", i, v)

    return features


def read_conll(loc, max_sent=None, use_coarse_pos=True):
    header = "ID FORM LEMMA CPOS FPOS X HEAD LABEL X X".split()

    sentences = []
    for ex in read_tabular_file(loc, header, max_sent):
        words = DefaultList([e["FORM"] for e in ex], default=None)
        heads = [e["HEAD"] for e in ex]
        
        cpos = DefaultList([e["CPOS"] for e in ex], default=None)
        fpos = DefaultList([e["FPOS"] for e in ex], default=None)
        lemma = DefaultList([e["LEMMA"] for e in ex], default=None)

        features = {"cpos": pad_tokens(cpos),
                    "fpos": pad_tokens(fpos),
                    "lemma": pad_tokens(lemma)}
                    
        labels = [None] + [e["LABEL"] for e in ex]
        heads = [None] + [int(h) if h != 0 else len(ex) + 1 for h in heads]

        #yield pad_tokens(words), features, heads, labels
        sentences.append((pad_tokens(words), features, heads, labels))
    return sentences


def read_tabular_file(filehandler, header, max_sent=None):
    """
    Read `max_sent` sentences from a tabular file.

    Generates, for each example:
    - the position of the token in the sentence
    - the tokenized sentence
    - the features associated to each token
    - the gold heads
    - the labels of the dependency tree
    """
    cur_obser = []
    for line in filehandler:

        line = line.strip().split()
        if not line:
            yield cur_obser
            cur_obser = []
            continue

        cur_obser.append(dict(zip(header, line)))

    if len(cur_obser) != 0:
        yield cur_obser


def pad_tokens(tokens):
    tokens.insert(0, '<start>')
    tokens.append('ROOT')
    return tokens


# ===============
# Main Interface
# ===============

def test_dependency_parser(parser, dataset, predict_pos_tags=False):
    """
    Estimate the UAS achieved by a parser on a dataset

    The UAS correspond to the Unlabeled accuary. Punctuation token are
    ignored.

    Parameters
    ----------

    - parser, an instance of Parser
      the dependency parser to evaluate

    - dataset, a list of example
      the dataset to consider

    - predict_pos_tags, a boolean
      if True, the POS tags given in the test are not considered and,
      during inference, the parser is used to predict them.
    """
    correct = 0
    n_words = 0

    for words, tags, gold_heads, gold_labels in dataset:
        if not predict_pos_tags:
            _, heads = parser.parse(words, tags)
        else:
            _, heads = parser.parse(words)

        # we have to convert enumerate to a list so that we can slice
        # it and avoid considering the padding symbols
        for i, w in list(enumerate(words))[1:-1]:
            if gold_labels[i] in ('P', 'punct'):
                continue
            if heads[i] == gold_heads[i]:
                correct += 1
            n_words += 1

    return correct / n_words



def train_dependency_parser(parser, train_set, dev_set, n_epoch):
    """
    Trains a dependency parser.

    Parameters
    ----------

    - parser, an instance of Parser
            the dependency parser to train

    - train_set, a list of 4-tuple the training set. Each example is
            described by a 4-tuple (words, features, gold_parse,
            gold_label) in which `words` and `gold_label` are lists of
            strings, features is a dictionary of lists and gold_parse
            a list of int.
    
    - dev_set : development data

    - n_epoch, an integer
            the number of epochs to perform

    """
    for itn in range(n_epoch):
        corr = 0
        total = 0
        random.shuffle(train_set)

        for words, features, gold_parse, _ in train_set :
            # Here you should use the predicted tags
            corr += parser.train_online(words, gold_parse, pos_tags=features)
            total += len(words) - 1

        weights = copy(parser.model.weights)
        parser.model.average_weights()
        acc_test = test_dependency_parser(parser, dev_set)
        
        parser.model.weights = weights
        
        print("Epoch {} / {} : UAS train = {:.3%}, UAS dev = {:.3%}".format(itn+1, n_epoch, corr / total, acc_test))

    print('Averaging weights')
    parser.model.average_weights()


def check_projectivity(heads):
    """Check whether a dependency tree is projective or not.

    This methods implements the test described in [Gomez-Ródríguez and
    Nivre, 2010].

    [Gomez-Ródríguez and Nivre, 2010] A Transition-Based Parser for
    2-Planar Dependency Structures, ACL'10
    """
    from itertools import product

    # removes START symbol
    edges = [(j, i) for i, j in enumerate(heads)][1:]
    for (i, k), (j, l) in product(edges, repeat=2):
        if min(i, k) >= min(j, l):
            continue

        if min(i, k) < min(j, l) < max(i, k) < max(j, l):
            return False

    return True
