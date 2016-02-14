__author__ = 'korantin'

from Pointeur import Pointeur

class Item(object):
    def __init__(self, address, value):
        self.address = address
        self.value = value
        self.pointeurs = []
    def add_pointeur(self, pointeur):
        if isinstance(pointeur, Pointeur):
            pass

    def del_pointeur(self, pointeur):
        if isinstance(pointeur, Pointeur):
            pass
    def get_pointeur(self, pointeur):
        if isinstance(pointeur, Pointeur):
            pass
