# -*- coding:utf-8 -*-

class EventDispatcherEntry:

	def __init__(self,observer:callable,times:int = -1):

		assert callable(observer)
		assert type(times) == int

		self.times = times
		self.observer = observer

	def __setattr__(self,k,v):
		if k == "times":
			assert type(v) == int
			object.__setattr__(self,k,v)

		elif k == "observer":
			assert callable(v)
			object.__setattr__(self,k,v)
		else:
			raise AttributeError

	def __setitem__(self,k,v):
		self.__setattr__(k,v)

	def __getitem__(self,k):
		if k == "times":
			return self.times
		elif k == "observer":
			return self.observer
		else:
			raise AttributeError 

	# impossibilité de supprimer un attribut
	def __delattr__(self,k):
		raise AttributeError 

	def __delitem__(self,k):
		self.__delattr__(k)
