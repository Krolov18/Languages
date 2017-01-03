# coding: utf-8
# 123456 >>> 
# ["1","2","3","4","5","6"] >>> 
# [["1","2","3"],["4","5","6"]] >>> 
# [["1","100","2","10","3"],["4",100,"5",10,"6"]] >>>
# [["1","100","2","10","3"],["4",100,"5",10,"6"]] <<< a * 100 + b * 10 + c >>>

# 1 - chiffre to string
def chiffre2string(integer):
	return list(str(integer))


# 2 - segmener liste en 10**3
def segmenter_liste(liste):
	nvListe = []
	if len(liste)%3!=0:
		if len(liste)%3!=0:
			nvListe.append(liste[:len(liste)%3])
			reste=liste[len(liste)%3:]
		nvListe.extend([reste[3*x:3*(x+1)] for x in range(len(reste)//3)])
		return nvListe
	else:
		nvListe = [liste[3*x:3*(x+1)] for x in range(len(liste)//3)]
		return nvListe



# 3 - ajouter les milliers
def ajouter_milliers(liste):
	#2 > 1000 liste[-2]
	#3 > 1000 liste[-2] 1000000 liste[-4]
	#4 > 1000 liste[-2] 1000000 liste[-4] 1000000000 liste[-6]
	if len(liste) == 2:
		liste.insert(-1,"1000")
	elif len(liste) == 3:
		liste.insert(-1,"1000")
		liste.insert(-3,"1000000")
	elif len(liste) == 4:
		liste.insert(-1,"1000")
		liste.insert(-3,"1000000")
		liste.insert(-5,"1000000000")
	elif len(liste) == 5:
		liste.insert(-1,"1000")
		liste.insert(-3,"1000000")
		liste.insert(-5,"1000000000")
		liste.insert(-7,"1000000000000")
	elif len(liste) == 6:
		liste.insert(-1,"1000")
		liste.insert(-3,"1000000")
		liste.insert(-5,"1000000000")
		liste.insert(-7,"1000000000000")
		liste.insert(-9,"1000000000000000")
	return liste



def ajouter_dix_cent(liste):
	for element in liste:
		if isinstance(element,list):
			if len(element) == 3:
				element.insert(-1,"10")
				element.insert(-3,"100")
			elif len(element) == 2:
				element.insert(-1,"10")
	return liste

def ajouter_s(liste, exceptions):
	for element in liste:
		#print(element)
		if isinstance(element,list):
			if len(element) == 1:
				if element[0] == "1":
					element[0] = element[0]+"s"
			else:
				if (int(element[0]) * int(element[1]) == int(element[0])): (element[0],element[1])=element[0]+"s",element[1]+"s"
				elif (int(element[0]) * int(element[1]) == int(element[1])): element[0]=element[0]+"s"
				if (int(element[2]) * int(element[3]) == int(element[2])): (element[2],element[3])=element[2]+"s",element[3]+"s"
				elif (int(element[2]) * int(element[3]) == int(element[3])): element[2]=element[2]+"s"
				elif (int(element[2]) * int(element[3])) in exceptions.keys():
					element[2]= str(int(element[2]) * int(element[3]))
					element[3]=element[3]+"s"
				if element[4] == "0": element[4]=element[4]+"s"
				
	return liste

def effacer_element_nonDit(liste):
	nvlist = []
	for element in liste:
		if isinstance(element,list):
			nvlist.extend(element)
		else:
			nvlist.append(element)
	return [int(x) for x in nvlist if "s" not in x]

def traduire_chiffre2lettres(liste,dico):
	return [dico[x] for x in liste]

francais = {0:"zéro", 1:"un", 2:"deux", 3:"trois", 4:"quatre", 5:"cinq", 6:"six", 7:"sept", 8:"huit", 9:"neuf",10:"dix",11:"onze",12:"douze",13:"treize",14:"quatorze",15:"quinze",16:"seize",20:"vingt",30:"trente",40:"quarante",50:"cinquante",60:"soixante",70:"soixante-dix",71:"soixante-onze",72:"soixante-douze",73:"soixante-treize",74:"soixante-quatorze",75:"soixante-quinze",76:"soixante-zeize",77:"soixante-dix-sept",78:"soixante-dix-huit",79:"soixante-dix-neuf",80:"quatre-vingt",90:"quatre-vingt-dix",91:"quatre-vingt-onze",92:"quatre-vingt-douze",93:"quatre-vingt-treize",94:"quatre-vingt-quatorze",95:"quatre-vingt-quinze",96:"quatre-vingt-seize",97:"quatre-vingt-dix-sept",98:"quatre-vingt-dix-huit",99:"quatre-vingt-dix-neuf",100:"cent",1000000:"million",1000:"mille", 1000000000: "milliard"}

lister = traduire_chiffre2lettres(effacer_element_nonDit(ajouter_s(ajouter_dix_cent(ajouter_milliers(segmenter_liste(chiffre2string(999999999999)))),francais)),francais)
print(" ".join(lister))


# si le chiffre donné n'est pas dans le dictionnaire:
# faire tout le chemin suivant la langue dans laquelle on sera.
# Sinon renvoyer la valeur qu'il y a dans le dictionnaire.

