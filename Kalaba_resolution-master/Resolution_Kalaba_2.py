# coding: utf-8
import codecs, itertools, sys

def constituer_permutations(string):
	listeExt=[]
	for i in range(1,len(string)+1):
		listeInt = []
		for element in itertools.permutations(string,i):
			listeInt.append(element)
		listeExt.append(listeInt)
	return listeExt


def constituer_alphabet(phrases):
	liste = []
	for phrase in phrases:
		for lettre in phrase:
			if lettre not in liste:
				liste.append(lettre)
	return liste

def constituer_lexique(phrases):
	"""
		Le 'lexique' est un terme vague. un alphabet selon mon point de vue est un lexique.
		Un lexique peut regrouper toutes sortes d'éléments. Du plus petit au plus grand, nous aurons
		donc l'alphabet, les ngrams, 
	"""
	liste = []
	for phrase in phrases:
		phrase = phrase.strip().split(' ')
		for mot in phrase:
			if mot not in liste:
				liste.append(mot)
	return liste

def grouperElements(liste, function=len):
	lexique=[]
	data=sorted(liste, key=function)
	for k,g in itertools.groupby(data, function):
		lexique.append(list(g))
	return lexique

def diminuer_enumerate(liste):
	res=enumerate(liste[0])
	cpt = 1
	while cpt < len(liste):
		res = set(res)&set(enumerate(liste[cpt]))
		cpt+=1
	return sorted(list(res))

def diminuer(liste):
	res = liste[0]
	cpt = 1
	while cpt < len(liste):
		res = set(res)&set(liste[cpt])
		cpt+=1
	return sorted(list(res))

def diminuer_listes(liste1,liste2):
	liste = []
	for x in liste1:
		for y in liste2:
			liste.append(list(set(x)&set(y)))
	return [x for x in liste if x!=[]]

def recuperer_indices_identiques(couple):
	"""
		le couple doit avoir deux membre, un membre comparant et un à comparer.
		le premier membre est le comparant, le second le comparé
	"""	
	liste=[]
	#print(couple)
	for lettre in enumerate(couple[1]):
		liste.append(recuperer_indices(couple[0], lettre[1]))
	return liste

def recuperer_indices(mot,lettre):
	for indice, string in enumerate(mot):
		if string ==lettre:
			return indice

with codecs.open(sys.argv[1],"r","utf-8") as fichier:
	corpus = [ligne.strip() for ligne in fichier.readlines()]

alphabet = constituer_alphabet(corpus)
lexique = constituer_lexique(corpus)


# 1 tri du lexique par ordre alphabétique
#TriAlphabet = sorted(lexique)
# 2 regroupement des éléments du lexique par leur longueur
#TriLongueur = grouperElements(TriAlphabet,len)[1:]
#print(TriLongueur)


lexiquePermute = [x for x in itertools.permutations(lexique,2)]

indices = {x[0]:recuperer_indices_identiques(x) for x in lexiquePermute}
#for element in grouperElements(indices,function=lambda liste: liste):
	#print(element)
for element in indices:
	print(indices[element])


# par rapport au nombre de lettres dans le mot on fait une lambda qui regroupe par rapport à la position dans le mot à i position
# puis ces positions sont recoupées avec diminuer_listes




