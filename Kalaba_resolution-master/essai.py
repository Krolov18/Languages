__author__ = 'korantin'

from nltk.util import ngrams
from sys import argv
from itertools import *
from codecs import open
from yaml.representer import Representer
from yaml import load,dump,add_representer
from collections import defaultdict

def everygrams(sequence, min_len=1, max_len=-1,pad_left=False,pad_right=False):
    """

    Redéfinition de everygrams, afin de pouvoir avoir les pad_sides de disponibles

    Returns all possible ngrams generated from a sequence of items, as an iterator.

        >> sent = 'a b c'.split()
        >> list(everygrams(sent))
        [('a',), ('b',), ('c',), ('a', 'b'), ('b', 'c'), ('a', 'b', 'c')]
        >> list(everygrams(sent, max_len=2))
        [('a',), ('b',), ('c',), ('a', 'b'), ('b', 'c')]

    :param sequence: the source data to be converted into trigrams
    :type sequence: sequence or iter
    :param min_len: minimum length of the ngrams, aka. n-gram order/degree of ngram
    :type  min_len: int
    :param max_len: maximum length of the ngrams (set to length of sequence by default)
    :type  max_len: int
    :rtype: iter(tuple)
    """
    if max_len == -1:
        max_len = len(sequence)
    for n in range(min_len, max_len+1):
        for ng in ngrams(sequence, n, pad_left,pad_right):
            yield ng

class InfiniteDict(defaultdict):
    def __init__(self):
        defaultdict.__init__(self, self.__class__)

add_representer(InfiniteDict,Representer.represent_dict)

def main():
    poulet = InfiniteDict()
    with open("kalabaEnForme.yaml",'r','utf-8') as datas:
        corpus = load(datas)
            # assignation des bigrams aux kala qui les contient.
        for i in range(len(corpus)):
            for francais, kalaba in corpus:
                for gram in everygrams(francais,pad_left=True,pad_right=True):
                    if gram not in poulet:
                        poulet[gram] = [[i],[kalaba]]
                    elif (i not in poulet[gram][0]):
                        poulet[gram][0].append(i)
                        poulet[gram][1].append(kalaba)
            # for bigram in bigrams(francais,pad_right=True,pad_left=True):
            #     if bigram not in poulet:
            #         poulet[bigram] = [kalaba]
            #     elif kalaba not in poulet[bigram]:
            #         poulet[bigram].append(kalaba)
    print(poulet[('à', 'Nicole')])

    # for couple in deuxChasseurs:
    #     (string1,string2) = couple
    #     print(couple)
    #     temp = SequenceMatcher(None,string1[1],string2[1])
    #     temp1 = temp.get_matching_blocks()[1:]
    #     print(temp1)
if __name__ == '__main__':
    main()