__author__ = "Krolev"

import nltk
import sys
from nltk.parse.generate import generate, demo_grammar

parser = nltk.load_parser(sys.argv[1],format="fcfg")
for c  in parser.parse(["deux","gros","chats"]):
    print(c)