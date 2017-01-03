# coding: utf-8

import DocStringInheritance
import re
import NumberSyntax


class NumberSyntax20(NumberSyntax.NumberSyntax):

    @DocStringInheritance.DocInherit
    def p_e_1(self, p):
        if isinstance(p[3], str) and re.match(r'1?[0-9]', p[3]):
            return True
        elif isinstance(p[3], tuple):
            return True
        return False

    @DocStringInheritance.DocInherit
    def p_t(self, p):
        if not re.match(r'20', p[3]):
            return False
        return True


def main():
    c = NumberSyntax20()

if __name__ == '__main__':
    main()