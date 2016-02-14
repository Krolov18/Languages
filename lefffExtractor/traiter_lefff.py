# coding: utf-8

#import sqlite3
import re
import sys
import codecs
import yaml
#
#def creer_base():
	#for ligne in lexique:
		#if not ligne.startswith('#'):
			#(forme,categorie,syntaxe) = ligne.split('\t')
		#
#ligne = "apprêtions		v	[pred='apprêter_____1<suj:sn|sinf|scompl,obj:(sn)>',cat=v,@S1p]"
 #remordre_____1<suj:sn|sinf|scompl,obj:(sn)>
#print(ligne.strip('[]'))
#
#lexique = codecs.open(sys.argv[1],'r','latin-1')
#sortie = codecs.open(sys.argv[2],'w','latin-1')
#
#def recuperer_fonction(liste):
	#return [element.split(':')[0] for element in liste]
#
#def recuperer_info_lexique(lexique):
	#
	#return [forme, numero1, categorie, predicat, syntaxe, morphologie]
#listefinale=[]
#infosrecup = []
#for ligne in lexique:
	#morphology=[]
	#syntax={}
	#ligne = ligne.strip()
	#if not ligne.startswith('#') and not ligne.startswith('_'):
		#(forme,numero,categorie,syntaxe) = ligne.split('\t')
		#infosrecup.append(forme)
		#infosrecup.append(numero)
		#infosrecup.append(categorie)
		#if not "pred" in ligne and not '@f' in ligne:
			#lemme = forme
			#infosrecup.append(lemme)
		#if '[]' is syntaxe:
			#syntaxe = 'NULL'
			#infosrecup.append(syntaxe)
			#print(forme, syntaxe)
		#else:
			#syntaxe = syntaxe.strip('[]')
			#print(forme, syntaxe)
			#if not 'pred' in syntaxe:
				#print(forme, syntaxe)
				#if "," in syntaxe:
					#temp = syntaxe.split(',')
					#print(forme, temp)
					#for element in temp:
						#if '=' in element:
							#syntax.update({element.split('=')[0]:element.split('=')[1]})
							#infosrecup.append(syntax)
							#print(infosrecup)
							#print(forme, syntaxe, syntax)
						#elif '@f' in element:
							#if "être" in element or "avoir" in element:
								#lemme = element.strip('@f')
								#infosrecup.append(lemme)
								#print(forme, syntaxe, lemme)
						#elif '@' in element:
							#morphology.append(element.strip('@'))
							#print(forme, syntax, morphologie)
							#infosrecup.append(morphology)
						#infosrecup.append('NULL')
				#else:
					#if '=' in syntaxe:
						#syntax.update({syntaxe.split('=')[0]:syntaxe.split('=')[1]})
						#infosrecup.append(syntax)
						#print(forme, syntax)
					#if '@' in syntaxe:
						#morphology.append(syntaxe.strip('@'))
						#infosrecup.append(morphology)
						#print(lemme, morphology)
					#elif not '@' in syntaxe:
						#morphology = 'NULL'
						#infosrecup.append(morphology)
						#infosrecup.append('NULL')
				#print(lemme, morphology, syntax)
				#print(forme, categorie, numero, syntax, morphology)
			#else:
				#recherche = re.search("pred='(.*)'(.*)",syntaxe)
				#temp = recherche.group(1)
				#temp5 = recherche.group(2)
				#print(temp5)
				#numbers = '0123456789'
				#rec = re.search('__([0-9])',temp)
				#if rec:
					#print(rec.group(1))
					#(lemme,numero,tempor) = temp.partition(rec.group(1))
					#lemme = lemme.replace('_','')
					#for element in tempor.strip('<>').split(','):
						#if not ":" in element:
							#predicat = [tempor.strip('<>').split(',')]
						#else:
							#predicat = [{element.split(':')[0]:element.split(':')[1]} for element in tempor.strip('<>').split(',') if ':' in element]
					#infosrecup.append(predicat)
				#else:
					#print(temp)
					#predicat = {"predicat":temp}
					#infosrecup.append(predicat)
				#temp6 = temp5.split(',')
				#pronom=''
				#for el in temp6:
					#if '=' in el:
						#syntax.update({el.split('=')[0]:el.split('=')[1]})
						#infosrecup.append(syntax)
						#print(infosrecup)
						#print(forme, syntaxe, syntax)
					#elif '@f' in el:
						#if "être" in el or "avoir" in el:
							#lemme = el.strip('@f')
							#infosrecup.append(lemme)
							#print(forme, syntaxe, lemme)
					#elif '@' in el:
						#morphology.append(el.strip('@'))
						#print(forme, syntax, morphology)
					#
					#rec1=re.search("(Se)(<.*>)(.*)",tempor)
					#if rec1:
						#print(rec1.group(1))
						#print(rec1.group(3))
						#pronom = [{"pronom":rec1.group(1),"valeur":rec1.group(3)}]
					#else:
						#pronom = 'NULL'
				#infosrecup.append(pronom)
				#infosrecup.append(syntax)
				#infosrecup.append(morphology)
				#infosrecup.append(pronom)
						#print(yaml.dump(pronom, default_flow_style=False))
						#print(lemme, rec1.group(1),rec1.group(3),rec1.group(2))
	#listefinale.append(infosrecup)
	#print(infosrecup)
	#infosrecup = []
#print(listefinale[5])
#for element in listefinale:
	#if len(element) != 7:
		#print(element)

#forme, numero, categorie, construction, lemme, syntaxe, morphology

#def compter_type(liste,type):
	#i=0
	#for element in liste:
		#if isinstance(element,type):
			#i+=1
	#return i

def supprimer_type(liste, type):
	def compter_type():
		i=0
		for element in liste:
			if isinstance(element,type):
				i+=1
		return i

	for step in range(compter_type()):
		for element in liste:
			if isinstance(element,type):
				liste.remove(element)
	return liste

with codecs.open(sys.argv[1],'r','latin-1') as lexique:
	lexicon = []
	for ligne in lexique:
		if not ligne.startswith('#'):
			forme = {}
			(form, chiffre, categorie,construction) = ligne.split('\t')
			construction = construction.replace('=',': ')
			if "@" in construction:
				construction = construction.replace('@',"a@")
			research = re.search(": '(.*)'[,\]]",construction)
			if research:
				construction = construction.replace(research.group(1),research.group(1).replace("'",'"'))
			morpho = {"morphologie": []}
			construction = yaml.load(construction)
			for element in construction:
				if isinstance(element,str):
					morpho["morphologie"].append(element)
			construction.append(morpho)
			construction = supprimer_type(construction,str)
			for element in construction:
				#print(element)
				forme.update(element)
			forme.update({"forme":form})
			forme.update({"categorie":categorie})
			lexicon.append(forme)
with codecs.open(sys.argv[2],'w','utf-8') as stream:
	yaml.dump(lexicon,stream,default_flow_style=False,allow_unicode=True)
	print(yaml.dump(lexicon, default_flow_style=False,allow_unicode=True))





