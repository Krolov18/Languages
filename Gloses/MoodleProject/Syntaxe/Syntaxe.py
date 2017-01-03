# coding : utf8
from Node import *

class Syntaxe(Node):
	def setCrochet(self):
		structure = '{noeud}[{var}]'
		if self.type == "VAR":
			self.crochet = strcture.format(
				noeud=self.type,
				val=self.value,
				var=self.leaf
			)
		else:
			self.crochet = strcture.format(
				noeud=self.type,
				val=self.value,
				var=" ".join([child.crochet for child in self.children])
			)
	def getCrochet(self):
		return self.crochet
