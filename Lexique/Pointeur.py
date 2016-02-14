__author__ = 'korantin'

###########################
#
#
#
#
# Pointeur est un lien entre une connaissance
# dans la machine et un object abstrait utilisant
# cette connaissance.
# Instancier un pointeur c'est créer une connaissance
# si cette connaissance n'est pas encore connue
# sans quoi, le pointeur ne sert que de passerelle
# entre deux ou plusieurs connaissances
# Un pointeur ne peut pas exister intrinsèquement.
# Il existe grâce à au moins deux connaissances
#
#
#
#
###########################


class Pointeur(object):
    def __init__(self, value):
        self.value = value
        self.address = None
        pass
    def __repr__(self):
        return (self.address, self.value)
    def __del__(self):
        pass
    def __str__(self):
        print("Je pointe sur la donnée {self.value}".format(self=self))