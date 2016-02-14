from abc import ABCMeta, abstractmethod

class Decoupeur:
	"""
		Classe abstraite de Decoupeur
	"""
	__metaclass__ = ABCMeta
	@abstractmethod
	def decouper(self):
		pass
