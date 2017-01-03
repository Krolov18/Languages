Ce dossier en l'état actuel contient cinq fichiers python et un pickle.

    DocStringInheritance.py
    NumberLexicon.py
    NumberSyntax.py
    Parser.py
    Nombres.py

    exceptions.pickle

DocStringInheritance permet lors d'un héritage de classe, ou de méthode d'hériter de la doctring soit l'attribut __doc__

A des fin de réutilisabilité et généricité du code, le lexique et la syntaxe ont été implémentés
dans deux classes différentes.

Toujours à des fins de généricité du code, la classe Parser peut être vu comme une "base class" pour n'importe
quel parseur.

De ce fait, comme python permet l'héritage multiple, il suffit de créer une nouvelle classe, d'héritéer de
NumberLexicon, NumberSyntax et de Parser pour avoir un outil de parsing complet.
Pour cette dernière partie, dans une première version, le parseur sera contenu dans un seule classe.

Enfin Nombres contient une classe qui correspond à la boite à outils du programme.


############################################
#
# MODE D'EMPLOI
#
############################################

Le programme à pour but de prendre en entrée un entier "390" par exemple, et d'en sortir une chaine de caractères
correspondant dans une langue donnée "trois cent quatre vingt dix" pour le français.
Le programme peut aussi faire la réciproque. On peut lui donner "trois cent quatre vingt dix" et avoir en sortie "390".


Pour la version entier vers string, l'algorithme suit quatre étapes.

    1 - entier vers liste
    2 - chunking
    3 - ajouter les multiples
    4 - ajouter les symboles
    5 - parsing de 4 pour mettre en forme pré-finale
    6 - traduction alignée du chiffre vers une valeur bifaces graphie/phonologie

Pour la version string vers entier, l'algorithme suit N étapes.
    1 - ajouter les symboles
    2 - parsing pour faire le calcul et le retourner