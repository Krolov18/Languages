__author__ = 'krolev'

multiplicateurs = {"interne":{3:10,1:100},"externe":{0:1000,1:1000000,2:1000000000}}
# 123 456 789 987
liste = list(str(2251))
nvListe=[]
if len(liste)%3!=0:
    nvListe.append(liste[:len(liste)%3])
    reste=liste[len(liste)%3:]
nvListe.extend([reste[3*x:3*(x+1)] for x in range(len(reste)//3)])

for p in nvListe:
    if len(nvListe) == 1:
        nvListe.insert(-2,multiplicateurs["externe"][0])
    elif len(nvListe) == 2:
        nvListe.insert(-1,multiplicateurs["externe"][1])
        nvListe.insert(-2,multiplicateurs["externe"][0])
    elif len(nvListe) == 3:
        nvListe.insert(-1,multiplicateurs["externe"][0])
        nvListe.insert(-3,multiplicateurs["externe"][1])
    elif len(nvListe) == 4:
        nvListe.insert(-1,multiplicateurs["externe"][0])
        nvListe.insert(-3,multiplicateurs["externe"][1])
        nvListe.insert(-5,multiplicateurs["externe"][2])
print(nvListe)