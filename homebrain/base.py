"""
Contains some base primitives that provide basic flow logic for the messages.

Based on a stripped down version of base.py in ActivityWatch.
"""

from abc import abstractmethod
import json
import logging
import threading
from queue import Queue

from typing import Optional


class Event(dict):
    """
    Used to represents an message.
    """
    def __init__(self, **kwargs):
        super(Event, self).__init__()
        self.update(kwargs)

    @property
    def type(self) -> str:
        return self["type"]

    def to_json_str(self) -> str:
        return json.dumps(self)


class Agent(threading.Thread):
    nrAgents = 1  # Monotonically increasing count of agents created

    def __init__(self):
        self.id = self.nrAgents
        threading.Thread.__init__(self, name=self.identifier)
        self._mailbox = Queue()
        self.nrAgents += 1

    def post(self, msg):
        self._mailbox.put(msg)

    def next_event(self, timeout=None) -> Optional[Event]:
        return self._mailbox.get() if timeout is None else self._mailbox.get(True, timeout)

    @abstractmethod
    def run(self):
        pass

    def stop(self):
        # TODO: Set @abstractmethod later
        pass

    @property
    def identifier(self) -> str:
        """Identifier for agent, used in settings and as a module name shorter than the class name"""
        return "{}[{}]".format(self.__class__.__name__, self.id)
