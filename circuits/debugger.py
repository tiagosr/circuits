# Module:	debugger
# Date:		2nd April 2006
# Author:	James Mills, prologic at shortcircuit dot net dot au

"""
Debugger component used to debug each event in a system by printing
each event to sys.stderr or to a Logger Component instnace.

Example:

>>> from circuits import listener, Event, Component, Debugger, Manager
>>> class Foo(Component):
	...     @listener("foo")
...     def onFOO(self):
	...             print "Hello World"
... 
>>> manager = Manager()
>>> foo = Foo()
>>> debugger = Debugger()
>>> manager += foo
>>> manager += debugger
<Registered/registered (, )>
>>> manager.push(Event(1, 2, 3, a=1, b=2, c=3), "foo")
>>> manager.flush()
<Event/foo (1, 2, 3, a=1, c=3, b=2)>
Hello World
"""

import sys

from circuits.core import listener, Event, Component


class Debug(Event):
	"""Debug Event

	:param msg: Message to display
	:type msg: str
	"""


class Debugger(Component):
	"""Create a new Debugger Component

	Creates a new Debugger Component that filters all events in teh system
	printing each event to sys.stderr or a Logger Component.

	:var IgnoreEvents: list of events (str) to ignore
	:var IgnoreChannels: list of channels (str) to ignore
	:var enabled: Enabled/Disabled flag

	:param log: Logger Component instnace or None (*default*)
	"""

	IgnoreEvents = []
	IgnoreChannels = []

	enabled = True

	def __init__(self, *args, **kwargs):
		"initializes x; see x.__class__.__doc__ for signature"

		super(Debugger, self).__init__(*args, **kwargs)

		self.logger = kwargs.get("logger", None)

	@listener(type="filter")
	def onEVENTS(self, event, *args, **kwargs):
		"""Global Event Handler

		Event handler to listen and filter all events printing each event
		to sys.stderr or a Logger Component instnace. This behavior is
		controllbed by the :attr:`enabled flag <circuits.debugger.Debugger.enabled>`
		"""

		if self.enabled:
			channel = event.channel
			if True in [event.name == name for name in self.IgnoreEvents]:
				return
			elif channel in self.IgnoreChannels:
				return
			else:
				if self.logger:
					self.logger.debug(repr(event))
				else:
					print >> sys.stderr, event
