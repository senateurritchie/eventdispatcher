# -*- coding:utf-8 -*-

class Event:
	"""
	l'objet évènement qui contient les informations liées a un évènement spécifique
	"""

	def __init__(self,name:str, data):
		self.name = name
		self.data = data
		self.timestamp = None

	def __repr__(self):
		return '<Event name="{}"" data="{}" >'.format(self.name,self.data)