# coding : utf-8
from Node import *

class Logique(Node):
	def setXML(self):
		structure = '<{noeud} val="{val}">{var}</{noeud}>'
		if self.type == "VAR":
			self.xml = structure.format(
				noeud=self.type,
				val=self.value,
				var=self.leaf)
		else:
			self.xml = structure.format(
				noeud=self.type,
				val=self.value,
				var="".join([child.xml for child in self.children]))
	def setCrochet(self):
		structure = '({val}){noeud}[{var}]'
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
				var="".join([child.crochet for child in self.children])
			)

	def getXML(self):
		return self.xml

	def getCrochet(self):
		return self.crochet

	def normaliser(self):
		if self.head != "VAR":
			if self.type == "IMPL":
				self.normale = Node(
					type = "DISJ",
					children = [
						Node(
							type="NEG", 
							head="NEG", 
							children=[self.children[0]], 
							value=inverserChiffre(self.children[0].value),
							),
						self.children[1]
						],
					value = self.value)
			elif self.type == "REPIP":
				self.normale = Node(
					type = "CONJ",
					children = [
						Node(
							type="IMPL",
							head="IMPL",
							children=[self.children[0],self.children[1]],
							value=inverserChiffre(self.children[0].value) or self.children[1].value),
						Node(
							type="IMPL",
							head="IMPL",
							children=[self.children[1],self.children[0]],
							value=inverserChiffre(self.children[1].value) or self.children[0].value)
					],
					value = self.value)
			elif self.type == "NEG":
				if self.children[0].type == "NEG":
					self.normale = self.children[0].children
				elif self.children[0].type != "VAR":
					if self.children[0].type == "CONJ":
						self.normale = Node(
							type="DISJ",
							head="DISJ",
							children=[
								Node(
									type="NEG",
									head="NEG",
									children=[self.children[0].children[0]],
									value=inverserChiffre(self.children[0].children[0].value)),
								Node(type="NEG",
									head="NEG",
									children=[self.children[0].children[1]],
									value=inverserChiffre(self.children[0].children[1].value))
							],
							value=self.value
							)
					elif self.children[0] == "DISJ":
						self.normale = Node(
							type="CONJ",
							head="CONJ",
							children=[
								Node(
									type="NEG",
									head="NEG",
									children=[self.children[0].children[0]],
									value=inverserChiffre(self.children[0].children[0].value)),
								Node(type="NEG",
									head="NEG",
									children=[self.children[0].children[1]],
									value=inverserChiffre(self.children[0].children[1].value))
							],
							value=self.value
							)
			elif ((self.children[0].type=="VAR") and (self.children[1].type not in ["VAR","NEG"])):
				self.normale = Node(
					type=self.children[1].type,
					head=self.children[1].head,
					children=[
						Node(
							type=self.children[0].type,
							head=self.children[0].head,
							children=[self.children[0],self.children[1].children[0]],
							value=self.children[0].value and self.children[1].children[0].value),
						Node(type=self.children[0].type,
							head=self.children[0].head,
							children=[self.children[0],self.children[1].children[1]],
							value=self.children[0].value and self.children[1].children[1].value)
					],
					value=self.value
					)
			elif ((self.children[1].type=="VAR") and (self.children[0].type not in ["VAR","NEG"])):
				self.normale = Node(
					type=self.children[0].type,
					head=self.children[0].head,
					children=[
						Node(
							type=self.children[1].type,
							head=self.children[1].head,
							children=[self.children[1],self.children[0].children[0]],
							value=self.children[1].value and self.children[0].children[0].value),
						Node(type=self.children[1].type,
							head=self.children[1].head,
							children=[self.children[1],self.children[0].children[1]],
							value=self.children[1].value and self.children[0].children[1].value)
					],
					value=self.value
					)
