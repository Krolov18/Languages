# coding: utf-8

import ply.lex as lex

tokens = ("VAR","VAL")

literals = ["~","(",")","&","|",">","=","-"]

t_VAR = r'[A-Za-zäâêëîïôöûüçàèé]+'

def t_VAL(t):
	r'(0|1)'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Invalid Type : {0}".format(type(t.value)))
	return t

t_ignore = " \t"

def t_error(t):
	print ("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lex.lex()

