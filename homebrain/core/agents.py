"""
Contains some base primitives that provide basic flow logic for the messages.

Based on a stripped down version of base.py in ActivityWatch.
"""

from abc import abstractmethod, ABCMeta
import threading
from queue import Queue, Empty
from . import Event

from typing import Optional


class Agent(threading.Thread):
    """
    Base class for all agents.
    """
    __metaclass__ = ABCMeta

    nrAgents = 1  # Monotonically increasing count of agents created

    def __init__(self, event_timeout=0.2):
        self.id = self.nrAgents
        threading.Thread.__init__(self, name=self.identifier)
        self._mailbox = Queue()
        self.nrAgents += 1
        self.daemon = True
        self.timeout = event_timeout
        self._running = True

    @property
    def identifier(self) -> str:
        """Identifier for agent, used in settings and as a module name shorter than the class name"""
        return "{}[{}]".format(self.__class__.__name__, self.id)

    @property
    def running(self) -> bool:
        return self._running

    def run(self):
        try:
            while self.running:
                try:
                    event = self.next_event(timeout=self.timeout)
                    self.handle_event(event)
                except Empty:
                    pass
        finally:
            self.cleanup()

    def stop(self):
        """
        Stops the agent.
        Not guaranteed to stop since it relies on the implementation of the specific agent.
        """
        self._running = False

    # TODO: Decide on the final name for this method: "post", "post_event", "put_event" or something else?
    def put_event(self, event: Event):
        self._mailbox.put(event)

    def next_event(self, timeout: Optional[float] = None) -> Optional[Event]:
        """
        Retrieves the next event in the queue.
        Will block until event is available, unless timeout is set in which
        case it will wait a maximum amount of time and then return None.
        """
        if timeout is None:
            return self._mailbox.get()
        else:
            return self._mailbox.get(True, timeout=timeout)

    # TODO: make @abstractmethod without breaking everything
    def handle_event(self, event):
        raise NotImplementedError

    # TODO: make @abstractmethod without breaking everything
    def cleanup(self):
        """
        Performs final cleanup. Called when an agent has been stopped or encounters an unhandled exception.
        Can be overridden to perform cleanup tasks, just don't forget to call the superclasses cleanup method first!
        """
        pass


class PausableAgent(Agent):
    """
    A simple attempt at a pausable agent.
    A pausable agent can simply pause it's event processing and resume it
    at a later point in time without the need to instantiate a new thread.
    """

    def __init__(self, **kwargs):
        Agent.__init__(**kwargs)
        self._not_paused_flag = threading.Event()
        self._not_paused_flag.set()

    def run(self):
        try:
            while self.running:
                # If paused, wait for pause to end
                self._not_paused_flag.wait()

                try:
                    event = self.next_event(timeout=self.timeout)
                    self.handle_event(event)
                except Empty:
                    pass
        finally:
            self.cleanup()

    @property
    def is_paused(self):
        return not self._not_paused_flag.is_set()

    def pause(self):
        self._not_paused_flag.clear()

    def unpause(self):
        self._not_paused_flag.set()