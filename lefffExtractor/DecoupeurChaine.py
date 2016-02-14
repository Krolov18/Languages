from Decoupeur import Decoupeur

class DecoupeurChaine(Decoupeur):
	def __init__(self,chaine):
		self.chaine = chaine
		self.liste = []
	def decouper(self):
		return self.chaine.split()