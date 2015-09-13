"""
Contains some base primitives that provide basic flow logic for the messages.

Based on a stripped down version of base.py in ActivityWatch.
"""


from abc import abstractmethod
import json
import logging

import threading
from datetime import datetime, timedelta

from typing import Iterable, List, Set


class Message(dict):
    """
    Used to represents an message.
    """
    def __init__(self, **kwargs):
        dict.__init__(self)

        self.update(kwargs)

        msg = ""
        msg += "Logged message '{}':".format(tags)
        msg += "  Started: {}".format(self["start"])
        msg += "  Ended: {}".format(self["end"])
        msg += "  Duration: {}".format(self.duration)
        if "cmd" in self:
            msg += "  Command: {}".format(self["cmd"])
        logging.debug(msg)

    def to_json_str(self) -> str:
        data = self.to_json_dict()
        return json.dumps(data)


class Agent(threading.Thread):
    """Base class for Watchers, Filters and Watchers"""

    def __init__(self):
        # TODO: This will run twice for Filters which will run both Watcher.__init__ and Logger.__init__
        threading.Thread.__init__(self, name=self.__class__.__name__)

    @abstractmethod
    def run(self):
        pass

    def stop(self):
        raise NotImplementedError

    @property
    def identifier(self):
        """Identifier for agent, used in settings and as a module name shorter than the class name"""
        return self.name[0:-len(self.agent_type)].lower()


class Logger(Agent):
    """
    Base class for loggers

    Listens to watchers and/or filters and logs messages with a
    method that should be defined by the subclass.
    """

    def __init__(self):
        Agent.__init__(self)
        self.watchers = set()  # type: Set[Watcher]

        # Must be thread-safe
        self._messages = []
        self._messages_lock = threading.Lock()
        self._messages_in_queue_event = threading.Event()

    # Only here to keep editor from complaining about unimplemented method
    def run(self):
        while True:
            self.wait()
            messages = self.flush_messages()
            if len(messages) > 0:
                try:
                    self.log(messages)
                    logging.debug("{} logged {} messages".format(self.name, len(messages)))
                except Exception:
                    logging.error("An error occurred while trying to log messages, " +
                                  "readding {} messages to log-queue.".format(len(messages)), exc_info=True)
                    self.add_messages(messages)

    @abstractmethod
    def wait(self):
        """
        Usually runs `self.wait_for_messages()` or some other wait-condition.
        """

    @abstractmethod
    def log(self, messages: List[Message]):
        """
        Do whatever you wish to messages
        """

    # TODO: Use Optional[int] type annotation when the new mypy is on PyPI
    def wait_for_messages(self, timeout: int=None):
        """
        Blocks until there are messages in the queue
        to be retrieved with flush_messages
        """
        self._messages_in_queue_event.wait(timeout)

    @property
    def has_messages_in_queue(self) -> bool:
        return self._messages_in_queue_event.is_set()

    def add_message(self, message: Message):
        """
        Adds a single message to the queue
        """
        if not isinstance(message, Message):
            raise TypeError("{} is not an Message".format(message))
        with self._messages_lock:
            self._messages.append(message)
            self._messages_in_queue_event.set()

    def add_messages(self, messages: Iterable[Message]):
        """
        Adds an iterable of messages to the queue
        """
        for message in messages:
            self.add_message(message)

    def flush_messages(self) -> List[Message]:
        """
        Retrieves, removes and then returns all messages from the queue
        """
        with self._messages_lock:
            messages = self._messages
            self._messages = []
            self._messages_in_queue_event.clear()
        return messages

    def add_watcher(self, watcher: 'Watcher'):
        """
        Adds a watcher to the logger, if the logger isn't
        registered with the watcher it sets that up as well.
        """
        if not isinstance(watcher, Watcher):
            raise TypeError("{} is not a Watcher".format(watcher))

        self.watchers.add(watcher)
        if self not in watcher.loggers:
            watcher.add_logger(self)

    def add_watchers(self, watchers: 'Iterable[Watcher]'):
        """
        Does the same as add_watcher, but for an iterable of watchers.
        """
        for watcher in watchers:
            self.add_watcher(watcher)


class Watcher(Agent):
    """
    Base class for watchers

    Watches for messages with a method that should be defined by the
    subclass and forwards those messages to connected loggers and/or
    filters.
    """

    def __init__(self):
        Agent.__init__(self)
        self.loggers = set()  # type: Set[Logger]

    # Only here to keep editor from complaining about unimplemented method
    @abstractmethod
    def run(self):
        pass

    def add_logger(self, logger: Logger):
        """
        Adds a single logger to the watcher, if the watcher isn't
        registered with the logger it sets that up as well.
        """
        if not isinstance(logger, Logger):
            raise TypeError("{} was not a Logger".format(logger))

        self.loggers.add(logger)
        if self not in logger.watchers:
            logger.add_watcher(self)

    def add_loggers(self, loggers: Iterable[Logger]):
        for logger in loggers:
            self.add_logger(logger)

    def dispatch_message(self, message: Message):
        """
        Sends a single message to the queues of all listening loggers.
        """
        for logger in self.loggers:
            logger.add_message(message)

    def dispatch_messages(self, messages: Iterable[Message]):
        """
        Sends a iterable of messages to the queues of all listening loggers.
        """
        for logger in self.loggers:
            logger.add_messages(messages)


class Filter(Logger, Watcher):
    """
    Base class for filters

    Acts as both a logger and a watcher, effectively being able to do
    certain operations on the received messages before sending them
    forward in the chain.
    """

    def __init__(self):
        Logger.__init__(self)
        Watcher.__init__(self)

    @abstractmethod
    def process(self, messages: List[Message]) -> List[Message]:
        """
        Does a set of operations on the messages
        """
        pass

    @abstractmethod
    def wait(self):
        pass

    def log(self, messages: List[Message]):
        self.dispatch_messages(messages)

    def run(self):
        while True:
            self.wait()
            messages = self.flush_messages()
            if len(messages) == 0:
                continue

            try:
                messages = self.process(messages)
            except Exception as e:
                logging.error("Error while trying to process messages")
                break

            self.log(messages)
            logging.debug("{} dispatched {} messages".format(self.name, len(messages)))

