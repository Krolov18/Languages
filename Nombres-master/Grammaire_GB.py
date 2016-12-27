# coding: utf-8

from Parser import Parser
from Node import Node
import typing


class GrammarNumbers(Parser):
    """
        Classe à découper en au moins deux classes, le lexique, et la syntaxe
        afin de rendre ces classes modulables.
    """

    # Il faut voir dans le terme 'token' la notion abstraite 'lexeme', c'est à dire le représentant de plusieurs formes.
    # ainsi 'U' représentera 'deux', 'trois', 'cinq' et 'six'

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

    # Les variables et fonctions prefixées par 't_' signifient qu'elles sont lexicales au sens d'un parseur
    # Vous pouvez tester cette fonction en instanciant GrammaireNumbers et en lançant la fonction
    # lexicalise(data) héritée de Parser.
    # Elle restreint les éléments que nous pouvons utilisées

    # Une règle lexicale peut se présenter sont la forme d'une variable ou d'une fonction

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
    t_ET = r'et'
    t_PLURIEL = r's'

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
    def p_num(p):
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
    def p_mmmnum(p):
        """
            MMMNum : Milliards MMNum
                   | Milliards
        """
        p[0] = Node(
            pere="MMMNum",
            children=p[1:]
        )

    @staticmethod
    def p_mmnum(p):
        """
            MMNum : Millions MNum
                  | Millions
        """
        p[0] = Node(
            pere="MMNum",
            children=p[1:]
        )

    @staticmethod
    def p_mnum(p):
        """
            MNum : Milliers CNum
                 | Milliers
        """
        p[0] = Node(
            pere="MNum",
            children=p[1:]
        )

    @staticmethod
    def p_cnum(p):
        """
            CNum : CNum1
                 | U1
        """
        p[0] = Node(
            pere="CNum",
            children=p[1:]
        )

    @staticmethod
    def p_cnum1_1(p):
        """
            CNum1 : Centaine DNum
        """
        p[0] = Node(
            pere="CNum1",
            children=p[1:]
        )

    @staticmethod
    def p_cnum1_2(p):
        """
            CNum1 : Unite Centaines
        """
        p[0] = Node(
            pere="CNum1",
            children=p[1:]
        )

    @staticmethod
    def p_cnum1_3(p):
        """
            CNum1 : DNum1
        """
        p[0] = Node(
            pere="CNum1",
            children=p[1:]
        )

    @staticmethod
    def p_dnum1(p):
        """
            DNum1 : Dizaine Un1Unite
        """
        p[0] = Node(
            pere="DNum1",
            children=p[1:]
        )

    @staticmethod
    def p_un1unite(p):
        """
            Un1Unite : Un1
                     | Unite
        """
        p[0] = Node(
            pere="Un1Unite",
            children=p[1:]
        )

    @staticmethod
    def p_dnum1_1(p):
        """
            DNum1 : Dizaine8 UniVingt
        """
        p[0] = Node(
            pere="DNum1",
            children=p[1:]
        )

    @staticmethod
    def p_dnum1_2(p):
        """
            DNum1 : Dizaine8 PLURIEL
        """
        p[0] = Node(
            pere="DNum1",
            children=p[1:]
        )

    @staticmethod
    def p_dnum1_3(p):
        """
            DNum1 : D6 Un11UniVingt11
        """
        p[0] = Node(
            pere="DNum1",
            children=p[1:]
        )

    @staticmethod
    def p_un11univingt11(p):
        """
            Un11UniVingt11 : Un11
                           | UniVingt11
        """
        p[0] = Node(
            pere="Un11UniVingt11",
            children=p[1:]
        )

    @staticmethod
    def p_dnum1_4(p):
        """
            DNum1 : UniVingt1
        """
        p[0] = Node(
            pere="DNum1",
            children=p[1:]
        )

    @staticmethod
    def p_dnum(p):
        """
            DNum : DNum1
                 | U1
        """
        p[0] = Node(
            pere="DNum",
            children=p[1:]
        )

    @staticmethod
    def p_un11(p):
        """
            Un11 : ET U1
                 | ET UV1
        """
        p[0] = Node(
            pere="Un11",
            children=p[1:]
        )

    @staticmethod
    def p_un1(p):
        """
            Un1 : ET U1
        """
        p[0] = Node(
            pere="Un1",
            children=p[1:]
        )

    @staticmethod
    def p_unite(p):
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
    def p_univingt11_1(p):
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
    def p_univingt11_2(p):
        """
            UniVingt11 : D1 U7
        """
        p[0] = Node(
            pere="UniVingt11",
            children=p[1:]
        )

    @staticmethod
    def p_univingt1(p):
        """
            UniVingt1 : UniVingt11
                      | UV1
        """
        p[0] = Node(
            pere="UniVingt1",
            children=p[1:]
        )

    @staticmethod
    def p_univingt(p):
        """
            UniVingt : UniVingt1
                     | U1
        """
        p[0] = Node(
            pere="UniVingt",
            children=p[1:]
        )

    @staticmethod
    def p_dizaine(p):
        """
            Dizaine : D
                    | D2
        """
        p[0] = Node(
            pere="Dizaine",
            children=p[1:]
        )

    @staticmethod
    def p_dizaine8(p):
        """
            Dizaine8 : U4 D2
        """
        p[0] = Node(
            pere="Dizaine8",
            children=p[1:]
        )

    @staticmethod
    def p_centaine(p):
        """
            Centaine : Unite C
                     | C
        """
        p[0] = Node(
            pere="Centaine",
            children=p[1:]
        )

    @staticmethod
    def p_centaines(p):
        """
            Centaines : C PLURIEL
        """
        p[0] = Node(
            pere="Centaines",
            children=p[1:]
        )

    @staticmethod
    def p_milliers(p):
        """
            Milliers : CNum1 M
                     | M
        """
        p[0] = Node(
            pere="Milliers",
            children=p[1:]
        )

    @staticmethod
    def p_millions(p):
        """
            Millions : CNum MM
                     | MM
        """
        p[0] = Node(
            pere="Millions",
            children=p[1:]
        )

    @staticmethod
    def p_milliards(p):
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


def generate_latexfile(data: typing.Union[tuple, typing.List[str]], allinone=False):
    """
        Fonction qui génèrera soit un élément de data pour un fichier
        soit
        l'ensemble de data dans un fichier.
    :param data:
    :param filename:
    :return:
    """
    import codecs

    filename = ""



    body = """\\documentclass[a4paper,landscape]{{report}}
\\usepackage{{tikz}}
\\usepackage{{qtree}}
\\usepackage{{avm}}
\\usepackage{{ulem}}
\\begin{{document}}
    {0}
\end{{document}}"""

    tree = """\\begin{{figure}}
		\Tree
            {0[1]}
	\caption{{{0[0]}}}
	\end{{figure}}"""

    if isinstance(data, tuple):
        return body.format(tree.format(data))
    elif isinstance(data, list):
        if allinone:
            return body.format([tree.format(x) for x in data])
        else:
            return body.format("".join(map(lambda x: "\n\t"+tree.format(x))))
    else:
        raise TypeError('Pas le bon type')

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
    # p = "un million deux cent onze mille trois cent quatre vingts"
    q = "soixante et onze"
    # o = map(lambda x: generate_latexfile(x), map(lambda x: (x, d.parse(x)), (p, q)))
    # print(next(o))
    # print(next(o))
    # print(q, d.parse(q))
    print(generate_latexfile(list(map(lambda x: d.parse(x), ["onze", "quarante cinq mille deux cent soixante dix huit", "deux cent quatre vingt onze", "vingt et un mille cent un", "deux", "cent trois"])), allinone=True))
    print(generate_latexfile((q, d.parse(q))))


if __name__ == '__main__':
    main()
