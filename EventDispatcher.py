# -*- coding:utf-8 -*-
import time

from Event import Event
from EventDispatcherEntry import EventDispatcherEntry

class EventDispatcher:
	"""
	gestionnaire d'évènements
	"""

	def __init__(self):
		self._data_event_dispatcher = {}
		inspect = dir(self)

		for k in inspect:
			if not k.startswith("on_"):
				continue

			if k in self.__dict__:
				continue

			method = getattr(self,k)
			eventname = k[3:]
			self.on(eventname,method)


	def on(self,eventname:str,observer:callable,times:int = -1):
		"""
		permet de souscrire à un évènement 
		@param eventname est le nom de l'évènement à souscrire
		@param observer est le listener a connecter  cet évènement
		@param times est le nombre de fois cet évènement doit etre excecuter la valeur -1 est pour excecuter l'évènement indefinniment
		"""
		assert type(eventname) == str 
		eventname = eventname.lower()

		if eventname in self._data_event_dispatcher:
			self._data_event_dispatcher[eventname].append(EventDispatcherEntry(times=times,observer=observer))

		else:
			self._data_event_dispatcher[eventname] = [EventDispatcherEntry(times=times,observer=observer)]


		return self


	def once(self,eventname:str,observer:callable):
		"""
		permet de souscrire une seule fois à un évènement
		"""
		return self.on(eventname,observer,1)
		

	def off(self,eventname:str,observer:callable=None):
		"""
		permet de desouscrire à un évènement 
		@param eventname est ne nom d'evenement à desouscrire
		@param observer s'il est fourni supprimera le couple {eventname,observer}
		"""

		assert type(eventname) == str 
		if observer is not None:
			assert callable(observer) 

		eventname = eventname.lower()

		if eventname in self._data_event_dispatcher:
			entries = self._data_event_dispatcher[eventname]
			if observer is None: # suppression total de l'évènement
				del self._data_event_dispatcher[eventname]
			else: # suppression de l'observer pour cet évènement
				for i,entry in enumerate(entries):
					if entry.observer is observer:
						del self._data_event_dispatcher[eventname][i]
						if len(self._data_event_dispatcher[eventname]) == 0:
							del self._data_event_dispatcher[eventname]
						break


		return self


	def dispatch(self,eventname:str,data,observer:callable = None):
		"""
		permet d'executer un évènement 
		@param eventname est ne nom d'evenement à executer
		@param data est la donnée à passer à l'observer
		@param observer si fourni, sera le seul observer a etre executé
		"""

		assert type(eventname) == str 

		if observer is not None:
			assert callable(observer) 

		if not isinstance(data, Event):
			data = Event(eventname,data)

		data.timestamp = time.time()

		eventname = eventname.lower()

		if eventname in self._data_event_dispatcher:
			entries = self._data_event_dispatcher[eventname]
			if observer is None: # execution de tout les observers
				for entry in entries:

					ret = entry.observer(data)
					if entry.times != -1:
						entry.times = entry.times - 1

					if ret is not None:
						break
													
			else: # execution de l'observer specifié
				for entry in entries:
					if entry.observer is observer:
						entry.observer(data)
						break

			def _clean_entities(data:list):
				for entry in data:
					if entry.times == 0:
						self.off(eventname,entry.observer)
						_clean_entities(data)

			# nettoyage
			_clean_entities(entries)

		return self




	def hasEvent(self,eventname:str,observer:callable=None):
		"""
		permet de verifier qu'un dispatcher possede un évènement
		si @param observer est fourni alors on verifira que l'observer est lié a cet évènement
		"""
		
		assert type(eventname) == str 
		eventname = eventname.lower()

		if observer is not None:
			assert callable(observer)
			if eventname in self._data_event_dispatcher:
				for entry in self._data_event_dispatcher[eventname]:
					if entry.observer is observer:
						return True

		else:
			return eventname in self._data_event_dispatcher
	

	