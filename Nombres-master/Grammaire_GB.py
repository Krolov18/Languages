# coding: utf-8

from Parser import Parser
from Node import Node


class GrammarNumbers(Parser):
    tokens = (
        "ET",
        "PLURIEL",
        "U1",
        "U",
        "U4",
        "U7",
        "D1",
        "UV1",
        "UV",
        "D2",
        "D",
        "D6",
        "C",
        "M",
        "MM",
        "MMM"
    )

    t_U = r"deux|trois|cinq|six"
    t_U1 = r"une?"
    t_U4 = r"quatre"
    t_U7 = r"sept|huit|neuf"
    t_UV = r"douze|treize|quatorze|quinze|seize"
    t_UV1 = r"onze"
    t_D = r"trente|quarante|cinquante"
    t_D1 = r"dix"
    t_D2 = r"vingt"
    t_D6 = r"soixante"
    t_C = r"cent"
    t_M = r"mille"
    t_MM = r"million"
    t_MMM = r"milliard"

    @staticmethod
    def t_ET(t):
        r"""et"""
        return t

    @staticmethod
    def t_PLURIEL(t):
        r"""s"""
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
    def p_Num(p):
        """
            Num : MMMNum
                | MMNum
                | MNum
                | CNum
        """
        p[0] = Node(
            pere="Num",
            children=p[1:]
        )

    @staticmethod
    def p_MMMNum(p):
        """
            MMMNum : Milliards MMNum
                   | Milliards
        """
        p[0] = Node(
            pere="MMMNum",
            children=p[1:]
        )

    @staticmethod
    def p_MMNum(p):
        """
            MMNum : Millions MNum
                  | Millions
        """
        p[0] = Node(
            pere="MMNum",
            children=p[1:]
        )

    @staticmethod
    def p_MNum(p):
        """
            MNum : Milliers CNum
                 | Milliers
        """
        p[0] = Node(
            pere="MNum",
            children=p[1:]
        )

    @staticmethod
    def p_CNum(p):
        """
            CNum : CNum1
                 | U1
        """
        p[0] = Node(
            pere="CNum",
            children=p[1:]
        )

    @staticmethod
    def p_CNum1_1(p):
        """
            CNum1 : Centaine DNum
        """
        p[0] = Node(
            pere="CNum1",
            children=p[1:]
        )

    @staticmethod
    def p_CNum1_2(p):
        """
            CNum1 : Unite Centaines
        """
        p[0] = Node(
            pere="CNum1",
            children=p[1:]
        )

    @staticmethod
    def p_CNum1_3(p):
        """
            CNum1 : DNum1
        """
        p[0] = Node(
            pere="CNum1",
            children=p[1:]
        )

    @staticmethod
    def p_DNum1(p):
        """
            DNum1 : Dizaine Un1Unite
        """
        p[0] = Node(
            pere="DNum1",
            children=p[1:]
        )

    @staticmethod
    def p_Un1Unite(p):
        """
            Un1Unite : Un1
                     | Unite
        """
        p[0] = Node(
            pere="Un1Unite",
            children=p[1:]
        )

    @staticmethod
    def p_DNum1_1(p):
        """
            DNum1 : Dizaine8 UniVingt
        """
        p[0] = Node(
            pere="DNum1",
            children=p[1:]
        )

    @staticmethod
    def p_DNum1_2(p):
        """
            DNum1 : Dizaine8 PLURIEL
        """
        p[0] = Node(
            pere="DNum1",
            children=p[1:]
        )

    @staticmethod
    def p_DNum1_3(p):
        """
            DNum1 : D6 Un11UniVingt11
        """
        p[0] = Node(
            pere="DNum1",
            children=p[1:]
        )

    @staticmethod
    def p_Un11UniVingt11(p):
        """
            Un11UniVingt11 : Un11
                           | UniVingt11
        """
        p[0] = Node(
            pere="Un11UniVingt11",
            children=p[1:]
        )

    @staticmethod
    def p_DNum1_4(p):
        """
            DNum1 : UniVingt1
        """
        p[0] = Node(
            pere="DNum1",
            children=p[1:]
        )

    @staticmethod
    def p_DNum(p):
        """
            DNum : DNum1
                 | U1
        """
        p[0] = Node(
            pere="DNum",
            children=p[1:]
        )

    @staticmethod
    def p_Un11(p):
        """
            Un11 : ET U1
                 | UV1
        """
        p[0] = Node(
            pere="Un11",
            children=p[1:]
        )

    @staticmethod
    def p_Un1(p):
        """
            Un1 : ET U1
        """
        p[0] = Node(
            pere="Un1",
            children=p[1:]
        )

    @staticmethod
    def p_Unite(p):
        """
            Unite : U
                  | U4
                  | U7
        """
        p[0] = Node(
            pere="Unite",
            children=p[1:]
        )

    @staticmethod
    def p_UniVingt11_1(p):
        """
            UniVingt11 : Unite
                       | D1
                       | UV
        """
        p[0] = Node(
            pere="UniVingt11",
            children=p[1:]
        )

    @staticmethod
    def p_UniVingt11_2(p):
        """
            UniVingt11 : D1 U7
        """
        p[0] = Node(
            pere="UniVingt11",
            children=p[1:]
        )

    @staticmethod
    def p_UniVingt1(p):
        """
            UniVingt1 : UniVingt11
                      | UV1
        """
        p[0] = Node(
            pere="UniVingt1",
            children=p[1:]
        )

    @staticmethod
    def p_UniVingt(p):
        """
            UniVingt : UniVingt1
                     | U1
        """
        p[0] = Node(
            pere="UniVingt",
            children=p[1:]
        )

    @staticmethod
    def p_Dizaine(p):
        """
            Dizaine : D
                    | D2
        """
        p[0] = Node(
            pere="Dizaine",
            children=p[1:]
        )

    @staticmethod
    def p_Dizaine8(p):
        """
            Dizaine8 : U4 D2
        """
        p[0] = Node(
            pere="Dizaine8",
            children=p[1:]
        )

    @staticmethod
    def p_Centaine(p):
        """
            Centaine : Unite C
                     | C
        """
        p[0] = Node(
            pere="Centaine",
            children=p[1:]
        )

    @staticmethod
    def p_Centaines(p):
        """
            Centaines : C PLURIEL
        """
        p[0] = Node(
            pere="Centaines",
            children=p[1:]
        )

    @staticmethod
    def p_Milliers(p):
        """
            Milliers : CNum1 M
                     | M
        """
        p[0] = Node(
            pere="Milliers",
            children=p[1:]
        )

    @staticmethod
    def p_Millions(p):
        """
            Millions : CNum MM
                     | MM
        """
        p[0] = Node(
            pere="Millions",
            children=p[1:]
        )

    @staticmethod
    def p_Milliards(p):
        """
            Milliards : CNum MMM
                      | MMM
        """
        p[0] = Node(
            pere="Milliards",
            children=p[1:]
        )

    @staticmethod
    def p_error(p):
        print("Syntax error at '%s'" % p.value)


def main():
    grammaire = """    Num → MMMNum | MMNum | MNum | CNum
    MMMNum → Milliards MMNum | Milliards
    MMNum → Millions MNum | Millions
    MNum → Milliers CNum | Milliers
    CNum → CNum1 | u1
    CNum1 → Centaine DNum
    CNum1 → Unite Centaines
    CNum1 → DNum1
    DNum1 → Dizaine Un1Unite
    Un1Unite → Un1 | Unite
    DNum1 → Dizaine8 UniVingt
    DNum1 → Dizaine8 PLURIEL
    DNum1 → d6 Un11UniVingt11
    Un11UniVingt11 → Un11 | UniVingt11
    DNum1 → UniVingt1
    DNum → DNum1 | u1
    Un11 → ET u1 | uv1
    Un1 → ET u1
    Unite → u | u4 | u7
    UniVingt11 → Unite | d1 | uv
    UniVingt11 → d1 u7
    UniVingt1 → UniVingt11 | uv1
    UniVingt → UniVingt1 | u1
    Dizaine → d | d2
    Dizaine8 → u4 d2
    Centaine → Unite c | c
    Centaines → c PLURIEL
    Milliers → CNum1 m | m
    Millions → CNum mm | mm
    Milliards → CNum mmm | mmm"""


    l = """
    u1 : un
    u1 : une
    u : deux
    u : trois
    u4 : quatre
    u : cinq
    u : six
    u7 : sept
    u7 : huit
    u7 : neuf
    d1 : dix
    uv1 : onze
    uv : douze
    uv : treize
    uv : quatorze
    uv : quinze
    uv : seize
    d2 : vingt
    d : trente
    d : quarante
    d : cinquante
    d6 : soixante
    c : cent
    m : mille
    mm : million
    mmm : milliard
    """

    # print("|".join([x.split(' : ')[1] for x in l.splitlines() if x != ""]))

    f = '''
        @staticmethod
        def p_{0}(p):
            """
                {1}
            """
            p[0] = p[1:]
    '''
    # print(grammaire)
    # [print(f.format(x.split(' → ')[0].strip(), x.strip().replace('→', ':')), end="") for x in grammaire.splitlines() if x != ""]

    d = GrammarNumbers()
    # for i in range(999999999999):
    #     pass
    print(d.parse("un million deux cent onze mille trois cent quatre vingts"))


if __name__ == '__main__':
    main()
