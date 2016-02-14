__author__ = 'krolev'
y='''
class Nombres:
    """
    1 - système 10^3 = on découpe l'intégral en séquences de trois unités avec un séquence incomplète à gauche si le reste
    de la division est différent de 0.

    Distinguons deux systèmes de représentations chiffrés. Le système court et le système long.

    Cette classe prend un chiffre integer (1, 433, 896) le parse selon la convention mathématique par centaines

    123456 >>> [(123), (456)]

    pour ensuite prendre ces constituants regroupés et les redécouper en éléments seuls et les convertit en string

    [(123), (456)] >>> [('1','2','3'), ('4','5','6')]

    Ainsi donc nous aurons en sortie une liste de tuples contenants chacuns des chaines de caractères.
    """
    #multiplicateurs = {2:0,1:10,0:100,1000,1000000,1000000000}
    def __init__(self,integer):
        self.integer = integer
        self.nvListe=[]
        self.liste = list(str(self.integer))

    def decomposer_chiffres(self):
        """
            Cette méthode prend un chiffre et en fait ressortir une liste.
            exemple : 123456789 >>> [[1,2,3],[4,5,6],[7,8,9]]
        :return: liste
        """
        if len(self.liste)%3!=0:
            if len(self.liste)%3!=0:
                self.nvListe.append(self.liste[:len(self.liste)%3])
                reste=self.liste[len(self.liste)%3:]
            self.nvListe.extend([reste[3*x:3*(x+1)] for x in range(len(reste)//3)])
            return self.nvListe
        else:
            self.nvListe = [self.liste[3*x:3*(x+1)] for x in range(len(self.liste)//3)]
            return self.nvListe
'''
f='''
class systemes_chiffres(Nombres):
    def __init__(self, liste):
        """
        Transformation de liste [[n,n],[n,n,n],[n,n,n]] >>> [1000000000, [n, 10,n], 1000000,[n, 100, n, 10, n], 1000,[n, 100, n, 10, n]]
        123 >>> [[1,2,3]] >>> [1, 100, 2, 10, 3]
        :return:
        """
        self.multiplicateurs = {10:["dix","dis"],100:{"cent":"sâ"},1000:{"mille":"mil"},1000000:{"million":"miljô"},1000000000:{"milliard":"miljar"}}
        if len(liste) == 3:
            liste.insert(0,self.multiplicateurs[1000000000])
            liste.insert(2,self.multiplicateurs[1000000])
            liste.insert(4,self.multiplicateurs[1000000])
        elif len(liste) == 2:
            liste.insert(0,self.multiplicateurs[1000000])
            liste.insert(2,self.multiplicateurs[1000])
        elif len(liste) == 1:
            liste.insert(0,self.multiplicateurs[1000])
        for element in liste:
            if isinstance(liste,list):
                if len(liste) == 3:
                    liste.insert(0,self.multiplicateurs[100])
                    liste.insert(2,self.multiplicateurs[10])
                    #liste.insert(4,self.multiplicateurs[0])
                elif len(liste) == 2:
                    liste.insert(0,self.multiplicateurs[10])
                    #liste.insert(2,self.multiplicateurs[0])
                elif len(liste) == 1:
                    #liste.insert(0,self.multiplicateurs[0])
        return liste


1234 >>> [[1],[2,3,4]]
Si la liste est entre 1 et trois éléments inclus, alors c'est le traitement centaines donc on applique l'algoritme :

une centaine vaut cela, donc "a * 100 + b * 10 + c" "{0} 100 {1} 10 {2}".format(a,b,c)




'''
r="""
class chiffre2graphie(Nombres):
    '''
    On hérite du découpage de Nombres et on génère une nouvelle méthode qui va actualiser la liste générée suivant
    la langue dans laquelle le texte veut-être.
    l'option langue dira au programme dans quelle langue le chiffre doit être formé.Nous utilisons la notation
    internationale pour les langue donc fr = français mais de = Deutsch (allemand)

    '''
    anglais = {0:"zero",1:"one",2:"two", 3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine",10:"ten",11:"eleven",12:"twelve",13:"thirteen",14:"fourteen",15:"fifteen",16:"sixteen",17:"seventeen",18:"eightenn",19:"nineteen"}
    allemand = {0:"null",1:"eins",2:"swei",3:"drei",4:"vier",5:"fünf",6:"sechs",7:"sieben",8:"acht",9:"neun",10:"zehn",}
    espagnol = {0:"cero",1:"uno",2:"dos",3:"tres",4:"cuatro",5:"cinco",6:"seis",7:"siete",8:"ocho",9:"nueve",10:"diez"}
    hollandais = {0:"null",1:"één",2:"twee",3:"drie",4:"vier",5:"vijf",6:"zes",7:"zeven",8:"acht",9:"negen",10:"tien",}
    latin = {1:"unus,uno,unum",2:"duo,duae,duo",3:"tres,tres,tria",4:"quattuor",5:"quinque",6:"sex",7:"septem",8:"octo",9:"novem",10:"decem/biquini",11:"undecim",12:"duodecim",13:"tredecim",14:"quattuordecim",15:"quindecim",16:"sedecim",17:"septemdecim",18:"duodeviginti",19:"undeviginti",20:"viginti",30:"triginta"}
    chinois = {0:"ling",1:"yi",2:"èr",3:"san",4:"si",5:"wu",6:"liu",7:"qi",8:"ba",9:"jiu",10:"shi",100:"bai",1000:"qian",10000:"wan",100000000:"yi",1000000000000:"zhao",10000000000000000:"jing"}
    yucateque = {1:"hun",2:"ca",3:"ox",4:"can",5:"ho",6:"uac",7:"uuc",8:"uaxac",9:"bolon",10:"lahun",20:"hunkal"}
    sinocoreen = {0:"yong",1:"il",2:"i",3:"sam",4:"sa",5:"o",6:"yuk",7:"ch'il",8:"p'al",9:"ku",10:"sip",100:"paek",1000:"ch'on",10000:"man",100000000:"ok",1000000000000:"cho",10000000000000000:"kyong",100000000000000000000:"hae",1000000000000000000000000:"cha",10000000000000000000000000000:"yang",100000000000000000000000000000000:"ku",1000000000000000000000000000000000000:"kan",10000000000000000000000000000000000000000:"chong",100000000000000000000000000000000000000000000:"chae",1000000000000000000000000000000000000000000000000:"kuk",10000000000000000000000000000000000000000000000000000:"hanghasa",100000000000000000000000000000000000000000000000000000000:"asunggi",1000000000000000000000000000000000000000000000000000000000000:"nayut'a",10000000000000000000000000000000000000000000000000000000000000000:"pulgasaui",100000000000000000000000000000000000000000000000000000000000000000000:"muryangdaesu"}
    coreen = {1:"hana",2:"tul",3:"set",4:"net",5:"tasot",6:"yosot",7:"ilgop",8:"yodol",9:"ahop",10:"yol",100:"on",1000:"chumun",10000:"tumon",100000000:"chal",10000000000000000:"kol"}
    japonais = {0:"rei",1:"ichi",2:"ni",3:"san",4:"yon/shi",5:"go",6:"roku",7:"shichi/nana",8:"hachi",9:"kyû",10:"jû",100:"hyaku",1000:"sen"}
    romain = {1:"I",5:"V",10:"X",50:"L",100:"C",500:"D",1000:"M"}
    def __init__(self,integer):
        Nombres.__init__(self, integer)

    def actualiser_decoupage(self,langue = "fr"):
        if langue == "fr":
            unites = {0:["zéro","zero"], 1:["un","ê"], 2:["deux","d9"], 3:["trois","trwa"], 4:["quatre","katr"], 5:["cinq","cêk"], 6:["six","sis"], 7:["sept","sEt"], 8:["huit","Hit"], 9:["neuf","n9f"]}
            dizaines_simples = {10:["dix","dis"],20:["vingt","vê"],30:["trente","trât"],40:["quarante","karât"],50:["cinquante","sêkât"],60:["soixante","swasât"]}
"""

traduire(123) > [1,2,3] > [[1, 100], [2, 10, 3]]


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



def ajouter_multiple(liste):
    multiplicateurs = {10:10,100:100,1000:1000,1000000:1000000,1000000000:1000000000}
    #1 000, 1 000 000, [0 100 0 10 0], 1 000 000, [0 100 0 10 0], 1 000, [0 100 0 10 0]]
    if len(liste) == 2:
        liste.insert(-1,1000)
    elif len(liste) == 3:
        liste.insert(-1,1000)
        liste.insert(-3,1000000)
    elif len(liste) == 4:
        liste.insert(-1,1000)
        liste.insert(-3,1000000)
        liste.insert(-5,1000000000)
    for element in liste:
        if isinstance(element,list):
            if len(element) == 2:
                element.insert(-1,10)
            elif len(element) == 3:
                element.insert(-1,10)
                element.insert(-3,100)
    return liste

def logique2langue(liste, langue = 'francais'):
    francais = {0:"zéro", 1:"un", 2:"deux", 3:"trois", 4:"quatre", 5:"cinq", 6:"six", 7:"sept", 8:"huit", 9:"neuf",10:"dix",11:"onze",12:"douze",13:"treize",14:"quatorze",15:"quinze",16:"seize",20:"vingt",30:"trente",40:"quarante",50:"cinquante",60:"soixante",70:"soixante-dix",71:"soixante-onze",72:"soixante-douze",73:"soixante-treize",74:"soixante-quatorze",75:"soixante-quinze",76:"soixante-zeize",77:"soixante-dix-sept",78:"soixante-dix-huit",79:"soixante-dix-neuf",80:"quatre-vingt",90:"quatre-vingt-dix",91:"quatre-vingt-onze",92:"quatre-vingt-douze",93:"quatre-vingt-treize",94:"quatre-vingt-quatorze",95:"quatre-vingt-quinze",96:"quatre-vingt-seize",97:"quatre-vingt-dix-sept",98:"quatre-vingt-dix-huit",99:"quatre-vingt-dix-neuf",100:"cent"}
    anglais = {0:"zero",1:"one",2:"two", 3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine",10:"ten",11:"eleven",12:"twelve",13:"thirteen",14:"fourteen",15:"fifteen",16:"sixteen",17:"seventeen",18:"eightenn",19:"nineteen"}
    allemand = {0:"null",1:"eins",2:"swei",3:"drei",4:"vier",5:"fünf",6:"sechs",7:"sieben",8:"acht",9:"neun",10:"zehn",}
    espagnol = {0:"cero",1:"uno",2:"dos",3:"tres",4:"cuatro",5:"cinco",6:"seis",7:"siete",8:"ocho",9:"nueve",10:"diez",11:"once",12:"doce",13:"trece",14:"catorce",15:"quince",16:"dieciseis",17:"diecisiete",18:"dieciocho",19:"diecinueve"}
    hollandais = {0:"null",1:"één",2:"twee",3:"drie",4:"vier",5:"vijf",6:"zes",7:"zeven",8:"acht",9:"negen",10:"tien",}
    latin = {1:"unus,uno,unum",2:"duo,duae,duo",3:"tres,tres,tria",4:"quattuor",5:"quinque",6:"sex",7:"septem",8:"octo",9:"novem",10:"decem/biquini",11:"undecim",12:"duodecim",13:"tredecim",14:"quattuordecim",15:"quindecim",16:"sedecim",17:"septemdecim",18:"duodeviginti",19:"undeviginti",20:"viginti",30:"triginta"}
    chinois = {0:"ling",1:"yi",2:"èr",3:"san",4:"si",5:"wu",6:"liu",7:"qi",8:"ba",9:"jiu",10:"shi",100:"bai",1000:"qian",10000:"wan",100000000:"yi",1000000000000:"zhao",10000000000000000:"jing"}
    yucateque = {1:"hun",2:"ca",3:"ox",4:"can",5:"ho",6:"uac",7:"uuc",8:"uaxac",9:"bolon",10:"lahun",20:"hunkal"}
    sinocoreen = {0:"yong",1:"il",2:"i",3:"sam",4:"sa",5:"o",6:"yuk",7:"ch'il",8:"p'al",9:"ku",10:"sip",100:"paek",1000:"ch'on",10000:"man",100000000:"ok",1000000000000:"cho",10000000000000000:"kyong",100000000000000000000:"hae",1000000000000000000000000:"cha",10000000000000000000000000000:"yang",100000000000000000000000000000000:"ku",1000000000000000000000000000000000000:"kan",10000000000000000000000000000000000000000:"chong",100000000000000000000000000000000000000000000:"chae",1000000000000000000000000000000000000000000000000:"kuk",10000000000000000000000000000000000000000000000000000:"hanghasa",100000000000000000000000000000000000000000000000000000000:"asunggi",1000000000000000000000000000000000000000000000000000000000000:"nayut'a",10000000000000000000000000000000000000000000000000000000000000000:"pulgasaui",100000000000000000000000000000000000000000000000000000000000000000000:"muryangdaesu"}
    coreen = {1:"hana",2:"tul",3:"set",4:"net",5:"tasot",6:"yosot",7:"ilgop",8:"yodol",9:"ahop",10:"yol",100:"on",1000:"chumun",10000:"tumon",100000000:"chal",10000000000000000:"kol"}
    japonais = {0:"rei",1:"ichi",2:"ni",3:"san",4:"yon/shi",5:"go",6:"roku",7:"shichi/nana",8:"hachi",9:"kyû",10:"jû",100:"hyaku",1000:"sen"}
    romain = {1:"I",5:"V",10:"X",50:"L",100:"C",500:"D",1000:"M"}
    polonais{0:"zero",1:"jeden",2:"dwa",3:"trzy",4:"cztery",5:"piêS",6:"szesc",7:"siedem",8:"osiem",9:"dziewiêS",10:"dziewiêS"}
    liste_finale = []

    # Partie "fr" : on découpe la liste interne en deux parties afin de gérer les exceptions.

    if langue == "francais":
        nvList = []
        #print(liste)
        for element in liste:
            if isinstance(element,list):
                if 100 in element:
                    element = découper_liste(element)
                    nvList.append(element)
                else:
                    nvList.append(element)
            else:
                nvList.append(element)

        for element in nvList:
            # verifier si resultat fait 0:
            if isinstance(element,list):
                if (len(element) == 3):
                    # si z*A+B vaut 0
                    if (int(element[0])*element[1])+int(element[2]) == 0:
                        nvList[nvList.index(element)] = 0
                    # si z*A+B dans francais.keys()
                    elif (int(element[0])*element[1])+int(element[2]) in francais.keys():
                        nvList[nvList.index(element)] = (int(element[0])*element[1])+int(element[2])
                    elif ((int(element[0])*element[1]) in francais.keys()):
                        nvList[nvList.index(element)] = [(int(element[0])*element[1]),int(element[2])]
                if (len(element) == 2):
                # si tout vaut 0
                    if ((int(element[0][0])*element[0][1])+((int(element[1][0])*element[1][1])+int(element[1][2]))) == 0:
                        nvList[nvList.index(element)] = 0
                    # si tout vaut qqch dans francais.keys()
                    elif (((int(element[0][0])*element[0][1])+((int(element[1][0])*element[1][1])+int(element[1][2]))) in francais.keys()):
                        nvList[nvList.index(element)] = ((int(element[0][0])*element[0][1])+((int(element[1][0])*element[1][1])+int(element[1][2])))
                    # si x*y vaut 0
                    elif ((int(element[0][0])*element[0][1]) == 0):
                        element[0] = 0
                    # si x*y dans francais.keys()
                    elif ((int(element[0][0])*element[0][1]) in francais.keys()):
                        element[0] = ((int(element[0][0])*element[0][1]))
                    # si z*A+B vaut 0
                    elif (int(element[1][0])*element[1][1])+int(element[1][2]) == 0:
                        element[1] = 0
                    # si z*A+B dans francais.keys()
                    elif (int(element[1][0])*element[1][1])+int(element[1][2]) in francais.keys():
                        element[1] = [(int(element[1][0])*element[1][1])+int(element[1][2])]
                    elif ((int(element[1][0])*element[1][1]) in francais.keys()):
                        element[1] = [(int(element[1][0])*element[1][1]),int(element[1][2])]



#    if langue == "deutsch":
#    if langue == "english":
#    if langue == "espagnol":
#    if langue == "hollandais":
#    if langue == "latin":
#    if langue == "chinois":
#    if langue == "yucatèque":
#    if langue == "sinocoreen":
#    if langue == "coreen":
#    if langue == "japonais":
#    if langue == "romain":

    return nvList


def découper_liste(liste, chunk=2):
    length = len(liste)
    return [liste[i*length // chunk: (i+1)*length // chunk] for i in range(chunk)]


integer = 4400000
liste = list(str(integer))
#print(liste)
#print(ajouter_multiple(segmenter_liste(liste)))
result = logique2langue(ajouter_multiple(segmenter_liste(liste)))

print(result)

def normaliser_liste(liste):
    nvList = []
    for x in liste:
        if isinstance(x,list):
            for y in x:
                if isinstance(y,list):
                    nvList.extend(y)
                else:
                    nvList.append(y)
        else:
            nvList.append(x)
    nvList = [int(element) for element in nvList]
    return [x for x in nvList if x!= 0]

def traduire_chiffre(chiffre,langue):
    if isinstance(chiffre,int):
        graphie = langue[chiffre]
        return graphie
    else:
        print("Je veux un intégral, pas %s" % (type(chiffre)))

def unite_mesure(liste):
    for element in liste:
        if element == "million" or element == "milliard":
            pattern = liste[0:3]
    return pattern

def accorder_nom(string):
    string = string+"s"
    return string

francais = {0:"zéro", 1:"un", 2:"deux", 3:"trois", 4:"quatre", 5:"cinq", 6:"six", 7:"sept", 8:"huit", 9:"neuf",10:"dix",11:"onze",12:"douze",13:"treize",14:"quatorze",15:"quinze",16:"seize",20:"vingt",30:"trente",40:"quarante",50:"cinquante",60:"soixante",70:"soixante-dix",71:"soixante-onze",72:"soixante-douze",73:"soixante-treize",74:"soixante-quatorze",75:"soixante-quinze",76:"soixante-zeize",77:"soixante-dix-sept",78:"soixante-dix-huit",79:"soixante-dix-neuf",80:"quatre-vingt",90:"quatre-vingt-dix",91:"quatre-vingt-onze",92:"quatre-vingt-douze",93:"quatre-vingt-treize",94:"quatre-vingt-quatorze",95:"quatre-vingt-quinze",96:"quatre-vingt-seize",97:"quatre-vingt-dix-sept",98:"quatre-vingt-dix-huit",99:"quatre-vingt-dix-neuf",100:"cent",1000:"mille",1000000:"million",1000000000:"milliard"}
r = [traduire_chiffre(x,francais) for x in normaliser_liste(result)]
print(r)
print(unite_mesure(r))
