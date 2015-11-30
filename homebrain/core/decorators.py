import functools
import logging
from typing import Callable
from . import Agent, Event


# Agent.handle_event() decorators


def stop_on_shutdown_event(f: Callable[[Agent, Event], None]):
    """
    Decorator which can be used to wrap the handle_event method.

    If a system_shutdown event is received, stop running without calling handle_event.
    """

    @functools.wraps(f)
    def wrapper(self, event, **kwargs):
        if event["type"] == "system_shutdown":
            self.stop()
        else:
            f(self, event, **kwargs)

    return wrapper


def log_events(f: Callable[[Agent, Event], None]):
    """
    Decorator which can be used to wrap the handle_event method.

    Logs every event that is handled.
    """

    @functools.wraps(f)
    def wrapper(self, event, **kwargs):
        logging.debug(event)
        f(self, event, **kwargs)

    return wrapper


def log_exceptions(f: Callable[[Agent, Event], None]):
    """
    Decorator which can be used to wrap the handle_event method.

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
