# coding: utf-8

import Lexicon


class NumberLexicon(Lexicon.Lexicon):
    tokens = ("NUMBER", "PLUS", "TIMES")

    literals = ('(', ')')

    t_PLUS = r'\+'
    t_TIMES = r'\*'
    t_NUMBER = r'\d+'
    t_ignore = r'\t\n '


def main():
    pass

if __name__ == '__main__':
    main()
