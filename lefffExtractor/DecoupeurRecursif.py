from DecoupeurChaine import DecoupeurChaine
import yaml

class DecoupeurRecursif(DecoupeurChaine):
    def decouper(self, separateurs):
        if len(separateurs[0]) == 3:
            (separator, side, number) = separateurs[0]
            if side == "l":
                temp = self.chaine.split(separator, number)
            elif side == "r":
                temp = self.chaine.rsplit(separator, number)
        elif len(separateurs[0]) == 2:
            if not isinstance(separateurs[0][0],str):
                raise TypeError("il ne peut pas y avoir autre chose qu'un string dans cette position.")
            else:
                (separator, side) = separateurs[0]
                if side == "l":
                    temp = self.chaine.split(separator)
                elif side == "r":
                    temp = self.chaine.rsplit(separator)
                elif side not in ["r","l"]:
                    raise TypeError("Cette position n'accepte que deux solutions 'l' ou 'r' et rien d'autre.")
        elif len(separateurs[0]) == 1:
            if not isinstance(separateurs[0][0],str):
                raise TypeError("il ne peut pas y avoir autre chose qu'un string dans cette position.")
            else:
                separator = separateurs[0][0]
                temp = self.chaine.split(separator)
        else:
            assert "il faut au moins 1 séparateur."
        if not any(x in y for x in [g[0] for g in separateurs] for y in temp) or len(separateurs) == 1:
            self.liste.append(tuple(temp))
        else:
            for element in temp:
                self.chaine = element
                self.decouper(separateurs[1:])

#if __name__ == '__main__':
#    essai = DecoupeurRecursif("bonjour,maman")
#    essai.decouper(',')
#    print(essai.liste)