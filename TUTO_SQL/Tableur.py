import sqlite3

class Tableur:
	def __init__(self,baseNom):
		self.container = sqlite3.connect(baseNom)
		self.containerCurseur = self.container.cursor()
	def commandeSimple(self, commande, *args):
		self.containerCurseur.execute(commande, args)
	def commandeMultiple(self, commande, args):
		self.containerCurseur.executemany(commande, args)
	def commandeScript(self, script):
		self.containerCurseur.executescript(script)
	def sauvegarderDonnees(self):
		self.container.commit()
	def fermerBase(self):
		self.container.close()
