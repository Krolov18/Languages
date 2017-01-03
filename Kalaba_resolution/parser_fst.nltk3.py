#!/usr/bin/env python
#coding=utf-8
"""
USAGE: python feature_parser.py FIC_GRAMMAIRE

       FIC_GRAMMAIRE est une grammaire CF augmentée de structures de traits (minimales, pas de disjonction, pas de négation)
"""

import sys
import nltk

default_encoding = 'utf-8'

HELP = \
"""
#  Commandes disponibles:
#  %help: affiche ce message
#  %reload_grammar: recharge le fichier grammaire et reconstruit un nouvel objet parser
#  %load_grammar FIC_GRAMMAIRE: charge FIC_GRAMMAIRE et construit un objet parser
#  %show_grammar: affichage de la grammaire.
#  %graphics: affiche un arbre graphique par analyse
#  %no_graphics: affiche les arbres uniquement au format texte (par défaut)
#  %exit: sort du programme
"""

def interpret_directive(s):
  global grammar_file
  if s == '%help':
    print HELP
  elif s == '%reload_grammar':
    load_grammar(grammar_file)
  elif s.startswith('%load_grammar'):
    grammar_file = s[s.index(' ')+1:]
    load_grammar(grammar_file)
  elif s == '%show_grammar':
    print parser.grammar()
  elif s == '%graphics':
    show_graphics(True)
  elif s == '%no_graphics':
    show_graphics(False)
  elif s == '%exit':
    sys.exit(0)
  else:
    print '# Commande %s non reconnue.' %s
    print '# Taper %help pour une liste des commandes disponibles.'

def load_grammar(f):
  global parser

  # Construction du parser pour la grammaire contenue dans fichier f
  parser = nltk.load_parser(f, format='fcfg')
  print "# Le fichier grammaire %s est chargé." %f

def show_graphics(b):
  global graphics
  graphics = b
  if graphics:
    print "# Arbres graphiques activés."
  else:
    print "# Arbres graphiques désactivés."

def boucle():
  global c,tp,tn,fp,fn
  # Objet Tokenizer
  tokenizer = nltk.tokenize.WordPunctTokenizer()

  # Boucle principale
  while 1:
    # Demande des phrases à analyser jusqu'à EOF ou %exit
    try:
      s = raw_input(prompt).strip().lower()

    except EOFError:
      break

    # Ignorer lignes vides et commentaires
    if not s or s.startswith('#'):
      continue
    elif s.startswith('%'):
      # les lignes commençant par % sont des commandes
      interpret_directive(s)
      continue

    # Tokenisation
    tokens = tokenizer.tokenize(s)
    # suppression des tokens '
    tokens = [x for x in tokens if x and not x == "'"]
    # Récupérer toutes les analyses
    try:
      #print "Je parse", tokens
      #print "..."
      parses=[]
      for p in parser.parse(tokens):
          parses.append(p)
    except ValueError, m:
      print '# PHRASE : %s' %(s)
      print '# %s'%m
      continue
    if parses:
      #print '# PHRASE : %s' %(s)
      #print '# %d ANALYSES POUR: %s' %len(parses), %(s)
      print "#",len(parses),"ANALYSES POUR:", s 
      for i,parse in enumerate(parses):
        print '# Analyse %s sur %s'%(i+1,len(parses))
        print parse

      if graphics:
#        draw_trees(*parses)
        for parse in parses:
          nltk.draw.draw_trees(parse)
    else:
      print '# PAS D\'ANALYSES POUR: %s' %(s)

if __name__ == '__main__':
  # Vérification fichier grammaire fourni
  if len(sys.argv) < 2:
    print "Le fichier de grammaire est manquant!"
    print __doc__
    sys.exit(1)

  # Construction de l'objet parser
  print
  print "# Bonjour!"
  print
  grammar_file = sys.argv[1]
  load_grammar(grammar_file)

  # pas de mode graphique par défaut
  show_graphics(False)
  if sys.stdin.isatty():
    prompt = '> '
  else:
    prompt = ''

  print "# Entrer une phrase à analyser."
  print "# Entrer %help pour les commandes disponibles."
  print

  boucle()
