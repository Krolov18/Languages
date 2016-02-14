from Decoupeur import Decoupeur

class DecoupeurChaine(Decoupeur):
	def __init__(self,chaine):
		self.chaine = chaine
	def decouper(self):
		return self.chaine.split()