# coding: utf-8
#struct = "({verite}){operateur}[{composantes}]"
#struct = "{syntagme}[{composantes}]"
#struct = "({fonction}){tete}[{composantes}]"

#(1)IMPL[(0)VAR[A] (1)VAR[B]]

#NP[(SG)DET[le] ADJ[grand] N[chien]]

#DP[Spec[] Dbar[D[le] NP[Spec[] Nbar[N[chien] Comp[]]]]]

#(root)chien[(det)le[] (mod)grand[]]

#ex="Paul mange une souris qui court dans l'herbe"

# langage Moodle
# langage Syntaxe simplifiée
# langage Syntaxe de dépendance
# langage Syntaxe x"
# langage logique propositionnelle arborée


# langage logique propositionnelle arborée
import LogiqueLexer
tokens = LogiqueLexer.tokens

from Logique import Logique
import ply.yacc as yacc

def p_axiome(p):
	"S : '-' prop"
	p[0] = p[2]

def p_statement_assign(p):
	'prop : VAR "=" VAL'
	p[0] = Node(head="VAR",
				type="VAR",
				value=int(p[3]),
				leaf=p[1]
				)

def p_prop_CONJ(p):
	'''prop : prop "&" prop'''
	p[0] = Node(type="CONJ",
				head="CONJ",
				value=p[1].value and p[3].value,
				children=[p[1],p[3]]
				)


def p_prop_DISJ(p):
	"prop : prop '|' prop"
	p[0] = Node(type="DISJ",
				head="DISJ",
				value=p[1].value or p[1].value,
				children=[p[1],p[3]]
				)

def p_prop_IMPL(p):
	"prop : prop '>' prop"
	p[0] = Node(type="IMPL",
				head="IMPL",
				value=inverserChiffre(int(p[1].value)) or p[3].value,
				children=[p[1],p[3]]
				)

def p_prop_NEG(p):
	"prop : '~' prop"
	p[0] = Node(type="NEG",
				head="NEG",
				value=inverserChiffre(int(p[2].value)),
				children=[p[2]]
				)

def p_prop_group(p):
	"prop : '(' prop ')'"
	p[0] = p[2]

def p_error(p):
	if p:
		print ("Syntax error at '{0}'".format(p.value))
	else:
		print ("Syntax error at EOF")

yacc.yacc()

from codecs import open

with codecs.open("formules.txt",'r','utf-8') as formules:
	phrases = [("<!-- Phrase : {0} -->".format(ligne),yacc.parse(ligne.strip())) for ligne in formules]
with codecs.open("sortie.xml",'w','utf-8') as sortie:
	sortie.write(bs("<arbres>{0}</arbres>".format("\n".join(["\n".join([phrase[0],phrase[1].getCrochet()]) for phrase in phrases])),"xml"))
