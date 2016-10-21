# coding: utf-8

__author__ = "Korantin"


import ply.lex as lex

tokens = (
    'UNSPEC',
    'AFFIX',
    'CLITIC',
    'REDUPL',
    'GINFIX',
    'DINFIX',
    'CIRCONF1',
    'ABLAUT',
    'POLYSE',
    'GMORPH0',
    'DMORPH0',
    'PORTMA',
    'GINHER',
    'DINHER',
    'PHRASE',
    'TRAIT',
    'LEMME',
	'CIRCONF2'
)


t_UNSPEC    = r'\:'
t_AFFIX     = r'\-'
t_CLITIC    = r'\='
t_REDUPL    = r'\~'
t_GINFIX    = r'\<'
t_DINFIX    = r'\>'
t_CIRCONF1  = r'[0-9]'
t_ABLAUT    = r'\\'
t_POLYSE    = r'\/'
t_GMORPH0   = r'\['
t_DMORPH0   = r'\]'
t_PORTMA    = r'\.'
t_GINHER    = r'\('
t_DINHER    = r'\)'
t_PHRASE    = r'\_'
t_CIRCONF2  = r'\+'

def t_LEMME(t):
    r'[a-zéàè][a-zéàè]*'
    return t

def t_TRAIT(t):
    r'[A-Z1-9][A-Z]*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex(optimize=1,lextab="gloseur")

# data = 'pomme(M)-P'
#
# lexer.input(data)
#
#
# while True:
#     tok = lexer.token()
#     if not tok:
#         break      # No more input
#     print(tok)