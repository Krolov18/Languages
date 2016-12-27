# coding: utf-8


class Syntax(object):
    @staticmethod
    def p_error(p):
        print("Syntax error at '%s'" % p.value)


def main():
    c = Syntax()
    print(c)

if __name__ == '__main__':
    main()