# coding: utf-8

import ply.lex as lex


class NumberLexicon(object):
    tokens = (
        "UNIT",
        "ZERO",
        "PLUS",
        "TIMES"
    )

    t_PLUS = r'\+'
    t_TIMES = r'\*'
    t_ignore = ' \t'

    @staticmethod
    def t_UNIT(t):
        r"""(1|2|3|4|5|6|7|8|9)"""
        t.value = int(t.value)
        return t

    @staticmethod
    def t_ZERO(t):
        r"""0"""
        return t

    @staticmethod
    def t_newline(t):
        r"""\n+"""
        t.lexer.lineo += len(t.value)

    @staticmethod
    def t_error(t):
        print('Je ne peux pas reconnaitre {0}'.format(t.value[0]))
        t.lexer.skip(1)


def main():
    lexer = lex.lex(
        module=NumberLexicon
    )

    data = "3*10+3"

    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

if __name__ == '__main__':
    main()
