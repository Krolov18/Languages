# coding: utf-8

import itertools

temp = """
":{trait}"
"-{trait}"
"={trait}"
"~{trait}"
"<{trait}>"

"_{trait}"
"/{trait}"
"{trait}i"

"\\{trait}"
"\\{trait}"
"[{trait}]"
".{trait}"
"({trait})"
"""

def grouperElements(liste, function=len):
    return [list(g) for k,g in itertools.groupby(sorted(liste, key=function), function)]

DOC = """
        Le gloseur prend en entrée :
            (mot-forme (FM), lemme (L), forme phonologique découpée (FP), glose-locale (GL), glose-générale (GG) )

            Le but sera récursivement de fournir un fichier XML au format moodle pour forme:


            <ENTETE XML>
                <ENTETE QUESTION>
                    <ENTETE QUESTIONTEXT>
                        <ENTETE CDATA>
                            STRING correspondant à FM + FEEDBACK
                            SAC (RXC) correspondant à FP + FEEDBACK
                            SAC (RXC) correspondant soit à la GL ou la GG + FEEDBACK
                        <TAIL CDATA>
                    <TAIL QUESTIONTEXT>
                <TAIL QUESTION>
            <TAIL XML>

            à côté de cela, du fait que le champ SAC (ou RXC) permet une plus grande précision sur la demande de
            l'enseignant au niveau de la correction, on a choisi, bien entendu, de développer les feedbacks.

            Pour ce faire le FEEDBACK grandira au fur et à mesure des appels recursifs.

            Pour une glose :

                parler.IND.PRS.1PL-IND.PRS.1PL

            La chaine sera parsée suivant une grammaire, qui aura pour chaque règle, des instructions.

            Considérons une grammaire simple :

            M -> R TS         #M(ot), R(adical), T(erminaison)
            R -> LEMME
            R -> L TL
            TL -> GPOINTS
            GPOINTS -> GPOINT GPOINT GPOINT
            GPOINT -> "." TRAIT
            TS -> "-" T






"""


import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'UNSPEC',
    'AFFIX',
    'CLITIC',
    'REDUPL',
    'GINFIX',
    'DINFIX',
    'CIRCONF',
    'ABLAUT',
    'POLY',
    'GMORPH0',
    'DMORPH0',
    'PORTMA',
    'GINHER',
    'DINHER',
    'PHRASE',
    'TRAIT',
    'LEMME'
)
# A regular expression rule with some action code


# Regular expression rules for simple tokens
t_UNSPEC    = r'\:'
t_AFFIX     = r'\-'
t_CLITIC    = r'\='
t_REDUPL    = r'\~'
t_GINFIX    = r'\<'
t_DINFIX    = r'\>'
t_CIRCONF   = r'[0-9]'
t_ABLAUT    = r'\\'
t_POLY      = r'\/'
t_GMORPH0   = r'\['
t_DMORPH0   = r'\]'
t_PORTMA    = r'\.'
t_GINHER    = r'\('
t_DINHER    = r'\)'
t_PHRASE    = r'\_'

def t_LEMME(t):
    r'[a-zA-Z][a-zA-Z]*'
    return t

def t_TRAIT(t):
    r'[A-Z1-9][A-Z][A-Z]*'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex(optimize=1,lextab="gloseur")

# Test it out
data = 'aller.IND.FUT-IND.FUT-IND-FUT-3PL'

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)