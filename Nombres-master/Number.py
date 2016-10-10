# coding: utf-8

from Parser import Parser
from functools import reduce
from operator import mul, add


class Number(Parser):
    tokens = (
        "UNIT",
        "PLUS",
        "TIMES",
        "ZERO"
    )

    t_PLUS = r'\+'
    t_TIMES = r'\*'

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

    t_ignore = ' \t'

    @staticmethod
    def t_error(t):
        print('Je ne peux pas reconnaitre {0}'.format(t.value[0]))
        t.lexer.skip(1)

    @staticmethod
    def p_s(p):
        """
            S : T PLUS unit
              | T PLUS S
        """
        if not isinstance(p[3], list):
            p[3] = [p[3]]
        tmp = reduce(add, [reduce(mul, map(int, p[1])), reduce(add, map(int, p[3]))])
        print(tmp)
        solution = Parser.exception(tmp, 'français')
        if solution:
            p[0] = [tmp]
        else:
            p[0] = p[1] + p[3]

    @staticmethod
    def p_t(p):
        """
            T : S TIMES multi
              | unit TIMES multi
        """
        if not isinstance(p[1], list):
            p[1] = [p[1]]
        p[3] = [p[3]]
        tmp = reduce(mul, [reduce(add, p[1])] + p[3])
        solution = Parser.exception(tmp, 'français')
        if solution:
            p[0] = [tmp]
        else:
            p[0] = p[1] + p[3]

    @staticmethod
    def p_unit(p):
        """
            unit : UNIT
                 | ZERO
        """
        p[0] = p[1]

    @staticmethod
    def p_multi(p):
        """
            multi : UNIT zeros
        """
        if p[1] != 1:
            raise SyntaxError('Seul 1 est admis.')
        p[0] = int("".join([str(p[1])] + p[2]))

    @staticmethod
    def p_zeros(p):
        """
            zeros : ZERO
                  | ZERO zeros
        """
        import itertools
        if len(p) > 2:
            p[0] = list(itertools.chain(*[p[1]] + [p[2]]))
        else:
            p[0] = list(itertools.chain(*[p[1]]))

    @staticmethod
    def p_error(p):
        print("Syntax error at '%s'" % p.value)


def main():
    tmp = Number()
    #print(tmp.parse("3*1000000+3"))

if __name__ == '__main__':
    main()