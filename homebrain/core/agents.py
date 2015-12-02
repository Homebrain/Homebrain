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
        self.nrAgents += 1  # statically increase the number of agents created

        threading.Thread.__init__(self, name=self.identifier, daemon=True)
        self._mailbox = Queue()

        self._enabled = False
        self._wait_for_event_timeout = event_timeout
        self._processed_events = 0

    # TODO: Rename "identifier" to something less like the class attribute id
    @property
    def identifier(self) -> str:
        """Identifier for agent, used in settings and as a module name shorter than the class name"""
        return "{}[{}]".format(self.__class__.__name__, self.id)

    @property
    def running(self) -> bool:
        """Returns true if the agent is actually running, otherwise false"""
        return self.is_alive()

    @property
    def enabled(self) -> bool:
        """Returns true if the agent is supposed to be running, otherwise false"""
        return self._enabled

    @property
    def queue_size(self) -> int:
        """Doesn't guarrantee the exact size of the queue, see Queue.qsize() docs for more info"""
        return self._mailbox.qsize()

    @property
    def processed_events(self) -> int:
        """Returns how many events have been removed from the queue"""
        return self._processed_events

    def start(self, *args, **kwargs):
        self._enabled = True
        threading.Thread.start(self, *args, **kwargs)

    def run(self):
        try:
            while self.enabled:
                try:
                    event = self.next_event(timeout=self._wait_for_event_timeout)
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
        self._enabled = False

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
            event = self._mailbox.get()
        else:
            event = self._mailbox.get(True, timeout=timeout)

        if event is not None:
            self._processed_events += 1

        return event

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

    def to_json_dict(self):
        """Dumps information about the agent in a JSON-serializable format"""
        obj = {"name": self.identifier, "id": self.id,
                "status": self.running, "enabled": self.enabled,
                "queue_size": self.queue_size, "processed_events": self.processed_events}
        return obj


class PausableAgent(Agent):
    """
    A simple attempt at a pausable agent.
    A pausable agent can simply pause it's event processing and resume it
    at a later point in time without the need to instantiate a new thread.
    """
    # WARNING: NOT TESTED! PROBABLY NOT WORKING!

    def __init__(self, **kwargs):
        Agent.__init__(**kwargs)
        self._not_paused_flag = threading.Event()
        self._not_paused_flag.set()
        raise NotImplementedError

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
