# coding: utf-8

import NumberSyntax20
import NumberLexicon


class Base20(NumberLexicon.NumberLexicon, NumberSyntax20.NumberSyntax20):
    pass


def main():
    x = Base20()
    x.p_t_1((1, 2, 3, 4))


if __name__ == '__main__':
    main()
