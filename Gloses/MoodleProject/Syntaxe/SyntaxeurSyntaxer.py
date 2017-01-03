# coding : utf8

# Module de syntaxe simplifiée

import SyntaxeurLexer
tokens = SyntaxeurLexer.tokens

from Syntaxe import Syntaxe
import ply.yacc as yacc


def p_S1(p):
	"S : NP VP"
	p[0] = Syntaxe(
		type="Syntagme",
		head="S",
		children=[p[1],p[2]],
		feedback="Attention S, se réécrit en {0} et en {1}".format(p[1].head,p[2].head)
		)
def p_S2(p):
	"S : NP VP PP"
	p[0] = Syntaxe(
		type="Syntagme",
		head="S",
		children=[p[1],p[2],p[3]],
		feedback="Attention, S se réécrit en {0}, en {1} et en {2}.".format(p[1].head,p[2].head,p[3].head)
		)
def p_NP1(p):
	"NP : DET N"
	p[0] = Syntaxe(
		type="Syntagme",
		head="NP",
		children=[p[1],p[2]],
		feedback="Attention, S se réécrit en {0} et en {1}.".format(p[1].head,p[2].head)
		)
def p_NP2(p):
	"NP : DET A N"
	p[0] = Syntaxe(
		type="Syntagme",
		head="NP",
		children=[p[1],p[2],p[3]],
		feedback="Attention, NP se réécrit en {0}, {1} et {2}."
		)
def p_VP1(p):
	"VP : V"
	p[0] = Syntaxe(
		type="Syntagme",
		head="V",
		children=[p[1]],
		feedback="Attention, VP se réécrit en {0}.".format(p[1].head)
		)
def p_VP2(p):
	"VP : V NP"
	p[0] = Syntaxe(
		type="Syntagme",
		head="V",
		children=[p[1],p[2]],
		feedback="Attention, VP se réécrit en {0} et en {1}.".format(p[1].head,p[2].head)
		)
def p_VP3(p):
	"VP : V NP PP"
	p[0] = Syntaxe(
		type="Syntagme",
		head="V",
		children=[p[1],p[2],p[3]],
		feedback="Attention, VP se réécrit en {0}, {1} et en {2}.".format(p[1].head,p[2].head,p[3].head)
		)
def p_DET(p):
	"LEAF : DET"
	p[0] = Node(
		type="LEX",
		head="DET",
		leaf=p[1],
		feedback="Une projection lexicale attend un mot syntaxique."
		)
def p_NOUN(p):
	"LEAF : NOUN"
	p[0] = Node(
		type=,
		head=,
		leaf=p[1],
		feedback="Une projection lexicale attend un mot syntaxique."
		)
def p_PREP(p):
	"LEAF : PREP"
	p[0] = Node(
		type=,
		head=,
		leaf=p[1],
		feedback="Une projection lexicale attend un mot syntaxique."
		)
def p_VERB(p):
	"LEAF : VERB"
	p[0] = Node(
		type="LEX",
		head="V",
		leaf=p[1],
		feedback="Une projection lexicale attend un mot syntaxique."
		)
def p_ADJ(p):
	"LEAF : ADJ"
	p[0] = Node(
		type="LEX",
		head="A",
		leaf=p[1],
		feedback="Une projection lexicale attend un mot syntaxique."
		)
def p_ADV(p):
	"LEAF : ADV"
	p[0] = Node(
		type="LEX",
		head="ADV",
		leaf=p[1],
		feedback="Une projection lexicale attend un mot syntaxique."
		)
def p_CONJ(p):
	"LEAF : CONJ"
	p[0] = Node(
		type="LEX",
		head="CNJ",
		leaf=p[1],
		feedback="Une projection lexicale attend un mot syntaxique."
		)
