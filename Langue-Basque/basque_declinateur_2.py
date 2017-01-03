from yaml import load, dump
import sys
import codecs

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

stream = codecs.open(sys.argv[1], 'r','utf-8')

data = load(stream, Loader=Loader)
#print(data)
print(data["Noms"]["Cas"])
# ...

#output = dump(data, Dumper=Dumper)
#print(output)

ligne = "forme(;phonetique);defini;nombre;animeite;cas;"
# haran:
# 	
# 
# 
# 
# 
for base in lexique:
	flechi_nb = 
