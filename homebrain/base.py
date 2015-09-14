"""
Contains some base primitives that provide basic flow logic for the messages.

Based on a stripped down version of base.py in ActivityWatch.
"""


from abc import abstractmethod
import json
import logging
import threading
from datetime import datetime, timedelta
from queue import Queue

from typing import Iterable, List, Set

class Event(dict):
    """
    Used to represents an message.
    """
    def __init__(self, **kwargs):
        dict.__init__(self)
        self.update(kwargs)

    @property
    def type(self) -> str:
        return self["type"]

    def to_json_str(self) -> str:
        data = self.to_json_dict()
        return json.dumps(data)


class Agent(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._mailbox = Queue()
        self._subscriptions = ["system_shutdown"]

    def post(self, msg):
        self._mailbox.put(msg)

    def next_event(self):
        return self._mailbox.get()

    @property
    def subscriptions(self):
        return self._subscriptions

    @abstractmethod
    def run(self):
        pass

    def stop(self):
        raise NotImplementedError

    @property
    def identifier(self):
        """Identifier for agent, used in settings and as a module name shorter than the class name"""
        return self.name[0:-len(self.agent_type)].lower()
