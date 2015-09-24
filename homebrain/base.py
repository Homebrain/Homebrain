"""
Contains some base primitives that provide basic flow logic for the messages.

Based on a stripped down version of base.py in ActivityWatch.
"""

from abc import abstractmethod
import json
import logging
import threading
import functools
from queue import Queue, Empty

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
    """
    Base class for all agents.
    """
    nrAgents = 1  # Monotonically increasing count of agents created

    def __init__(self, event_timeout=0.2):
        self.id = self.nrAgents
        threading.Thread.__init__(self, name=self.identifier)
        self._mailbox = Queue()
        self.nrAgents += 1
        self.daemon = True
        self.timeout = event_timeout
        self.running = True

    def post(self, msg):
        self._mailbox.put(msg)

    def next_event(self, timeout=None) -> Optional[Event]:
        return self._mailbox.get() if timeout is None else self._mailbox.get(
            True, timeout)

    @property
    def identifier(self) -> str:
        """Identifier for agent, used in settings and as a module name shorter than the class name"""
        return "{}[{}]".format(self.__class__.__name__, self.id)

    def run(self):
        try:
            while self.running:
                try:
                    event = self.next_event(timeout=self.timeout)
                    self.handle_event(event)
                except Empty as e:
                    pass
        finally:
            self.cleanup()

    def stop(self):
        self.running = False

    def cleanup(self):
        """Performs final cleanup. Called when an agent has been stopped or encounters an unhandled exception."""
        pass

    def stop_on_shutdown_event(f):
        """
        Decorator which wraps the handle_event method.

        If a system_shutdown event is received, stop running without calling handle_event.
        """

        @functools.wraps(f)
        def wrapper(self, event, **kwargs):
            if event["type"] == "system_shutdown":
                self.stop()
            else:
                f(self, event, **kwargs)

        return wrapper

    def log_events(f):
        """
        Decorator which wraps the handle_event method.

        Logs every event that is handled.
        """

        @functools.wraps(f)
        def wrapper(self, event, **kwargs):
            logging.debug(event)
            f(self, event, **kwargs)

        return wrapper

    def log_exceptions(f):
        """
        Decorator which wraps the handle_event method.

        If loop was aborted due to an unhandled exception, log it.
        """

        @functools.wraps(f)
        def wrapper(self, event, **kwargs):
            try:
                f(self, event, **kwargs)
            except Exception as e:
                # TODO: Standardise logging
                logging.exception(e)

        return wrapper
