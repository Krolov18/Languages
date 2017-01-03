# coding: utf-8
import itertools
import codecs
### Lexique BDLexique; récupération colonne 0

with codecs.open('/home/krolev/Documents/Scrabble/bdlexique.txt','r','utf-8') as file:
	lexique = [x.strip().split(';')[0] for x in file.readlines()]

### Fonction qui crée toutes les permutations des lettres proposees.
def permuter_sequence(string, lexique):
	liste=[]
	for i in range(2,len(sequence)+1):
		liste.extend(["".join(y) for y in [j for j in itertools.permutations(sequence, i)] if y in lexique])
	return liste

def comparer_lexique(liste,lexique):
	return [element for element in liste if element in lexique]

def grouperElements(liste, function=len):
	"""
		fonctions qui groupe selon la fonction qu'on lui donne.
		Ainsi pour le kalaba comme pour les graphèmes, nous aurons
		besoin de la longueur,
	"""
	lexique=[]
	data=sorted(liste, key=function)
	for k,g in itertools.groupby(data, function):
		lexique.append(list(g))
	return lexique


sequence = "foirelib"

possibilites = permuter_sequence(sequence,lexique)
print('DONE')
#existantes = comparer_lexique(possibilites,lexique)
#print('DONE')
print(sorted(grouperElements(existantes,function=len)))
