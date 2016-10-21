# coding : utf8

import ply.lex as lex
import sqlite3
with sqlite3.connect("lexique.sql3") as lexique:
	curseur = lexique.cursor()

tokens = ("TETE","FEUILLE","DET","NOUN","PREP","VERB","ADJ","ADV","CONJ")

literals = "[]"

def t_FEUILLE(t):
	r'[A-Za-zäâêëîïôöûüçàèé]+'
	curseur.execute("SELECT categorie FROM lexique WHERE forme=?",t.value)
	if len(curseur.fetchall()) != 1:
		t.type = curseur.fetchall()
	else:
		t.type = curseur.fetchall()[0]

def t_TETE(t):
	r'[A-Z]+'

def t_error(t):
	print("Erreur lexicale: symbole '{0}' non reconnu.".format(t.value[0]))
	t.lexer.skip(1)

t_ignore = " \n\t"

lex.lex()
