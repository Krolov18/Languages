__author__ = "Krolev"


Nombres = {}
Dizaines = {}
#[Nombres.update({x:""}) for x in range(0,100000000000)]
centaines = {100:{"cent":"sâ"}}
milliers = {1000:{"mille":"mil"}}
millions = {1000000:{"million":"miljô"}}
milliards = {1000000000:{"milliard":"miljar"}}
dico ={}
def generer_dizaines(dico):
	unites = {0:["zéro","zero"], 1:["un","ê"], 2:["deux","d9"], 3:["trois","trwa"], 4:["quatre","katr"], 5:["cinq","cêk"], 6:["six","sis"], 7:["sept","sEt"], 8:["huit","Hit"], 9:["neuf","n9f"]}
	dizaines_simples = {10:["dix","dis"],20:["vingt","vê"],30:["trente","trât"],40:["quarante","karât"],50:["cinquante","sêkât"],60:["soixante","swasât"]}
	for i in range(0,100):
		if i < 10:
			dico[i] = [unites[i]]
		elif i == 10:
			dico[i] = [dizaines_simples[i]]
		elif i < 20:
			dico[i] = [dizaines_simples[10], unites[i-10]]
		elif i == 20:
			dico[i] = [dizaines_simples[i]]
		elif i < 30:
			dico[i] = [dizaines_simples[20], unites[i-20]]
		elif i == 30:
			dico[i] = [dizaines_simples[i]]
		elif i < 40:
			dico[i] = [dizaines_simples[30], unites[i-30]]
		elif i == 40:
			dico[i] = [dizaines_simples[i]]
		elif i < 50:
			dico[i] = [dizaines_simples[40], unites[i-40]]
		elif i == 50:
			dico[i] = [dizaines_simples[i]]
		elif i < 60:
			dico[i] = [dizaines_simples[50], unites[i-50]]
		elif i == 60:
			dico[i] = [dizaines_simples[i]]
		elif i < 70:
			dico[i] = [dizaines_simples[60], unites[i-60]]
		elif i == 70:
			dico[i] = [dizaines_simples[60], dizaines_simples[10]]
		elif i < 80 :
			dico[i] = [dizaines_simples[60], dizaines_simples[10], unites[i-70]]
		elif i == 80 :
			dico[i] = [unites[4], dizaines_simples[20]]
		elif i < 90 :
			dico[i] = [unites[4], dizaines_simples[20], unites[i-80]]
		elif i == 90 :
			dico[i] = [unites[4], dizaines_simples[20], dizaines_simples[10]]
		elif i < 100:
			dico[i] = [unites[4], dizaines_simples[20], dizaines_simples[10], unites[i-90]]

# 0:["zéro","zero"], 
unites = {1:["un","ê"], 2:["deux","d9"], 3:["trois","trwa"], 4:["quatre","katr"], 5:["cinq","sêk"], 6:["six","sis"], 7:["sept","sEt"], 8:["huit","Hit"], 9:["neuf","n9f"]}
exceptions = {11:["onze","ôz"],12:["douze","duz"],13:["treize","trEz"],14:["quatorze","katOrz"],15:["quinze","kêz"],16:["seize","sEz"]}
dizaines_simples = {10:["dix","dis"],20:["vingt","vê"],30:["trente","trât"],40:["quarante","karât"],50:["cinquante","sêkât"],60:["soixante","swasât"]}
#dizaines_complexes = 

generer_dizaines(Nombres)

for nombre in Nombres:
	if nombre in exceptions:
		Nombres[nombre] = [exceptions[nombre]]


[print(Nombres[x]) for x in Nombres]
	




a = """
unite = 0123456789
dizaine = 
centaine = 
millier = 
million = 
milliard = 




(centaine*
	(dizaine+
		(unite)))*

	(milliard+
		(centaine*
			(dizaine+
				(unite)))*
	(million+
		(centaine*
			(dizaine+
				(unite)))*
	(millier+
		(centaine*
			(dizaine+
				(unite))))))"""
				
