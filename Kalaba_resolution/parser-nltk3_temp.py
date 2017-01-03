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
#    Commandes disponibles:
#    %help: affiche ce message
#    %reload_grammar: recharge le fichier grammaire et reconstruit un nouvel objet parser
#    %load_grammar FIC_GRAMMAIRE: charge FIC_GRAMMAIRE et construit un objet parser
#    %show_grammar: affichage de la grammaire.
#    %graphics: affiche un arbre graphique par analyse
#    %no_graphics: affiche les arbres uniquement au format texte (par défaut)
#    %exit: sort du programme
"""

class Grammaire:
    def __init__(self,grammaire):
        self.grammaire = grammaire
        tokenizer = nltk.tokenize.WordPunctTokenizer()
        parser = self.load_grammar(self.grammaire)
        while 1:
            try:
                chaineTapee = input(prompt).strip().lower()
            except EOFError:
                break
            if not chaineTapee or chaineTapee.startswith('#'):
                continue
            elif chaineTapee.startswith('%'):
                self.interpret_directive(chaineTapee)
                continue
            tokens = [x for x in tokenizer.tokenize(chaineTapee) if x and not x == "'"]
            parses=[]
            for p in parser.parse(tokens):
                parses.append(p)
            if parses:
                print("#", len(parses), "ANALYSES POUR:", chaineTapee)
                for i, parse in enumerate(parses):
                    print('# Analyse %s sur %s'%(i+1,len(parses)))
                    print(parse)

                if graphics:
    #                draw_trees(*parses)
                    for parse in parses:
                        nltk.draw.draw_trees(parse)
            else:
                print '# PAS D\'ANALYSES POUR: %s' %(s)



    def interpret_directive(self,chaine):
        if chaine == '%help':
            print(HELP)
        elif chaine == '%reload_grammar':
            self.load_grammar(self.grammaire)
        elif chaine.startswith('%load_grammar'):
            self.load_grammar(chaine.partition(' ')[2])
        elif chaine == '%show_grammar':
            print(self.load_grammar(self.grammaire).grammar())
        elif chaine == '%graphics':
            show_graphics(True)
        elif chaine == '%no_graphics':
            show_graphics(False)
        elif chaine == '%exit':
            sys.exit(0)
        else:
            print ('# Commande {0} non reconnue.'.format(chaine))
            print ('# Taper %help pour une liste des commandes disponibles.')

    def load_grammar(self, grammaire):
        parser = nltk.load_parser(grammaire, format='fcfg')
        print ("# Le fichier grammaire {} est chargé.".format(grammaire))
        return parser
    def show_graphics(self,graphics):
        if graphics:
            print("# Arbres graphiques activés.")
        else:
            print("# Arbres graphiques désactivés.")
        return graphics



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
