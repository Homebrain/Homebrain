from homebrain import AgentManager, Dispatcher
from homebrain.base import Agent, Event
import unittest
import threading
import time
from unittest.mock import patch

WAIT_TIME = 0.02  # time to sleep while waiting for a thread to react


class MockAgent(Agent):
    def __init__(self):
        super(MockAgent, self).__init__()
        self.events = []

    @Agent.stop_on_shutdown_event
    @Agent.log_exceptions
    @Agent.log_events
    def handle_event(self, event):
        self.events.append(event)
        if event["type"] == "test_exception":
            raise RuntimeError("This exception is unexpected and not caught by handle_event itself")

    def cleanup(self):
        pass


class AgentTest(unittest.TestCase):
    def setUp(self):
        self.mock_agent = MockAgent()
        self.mock_agent.start()
        time.sleep(WAIT_TIME)

    def test_stops_on_shutdown_event(self):
        """Since the handle_event method is decorated with @stop_on_shutdown_event, a system_shutdown event should stop the thread."""
        self.assertEquals([], self.mock_agent.events)
        self.mock_agent.post(Event(type="system_shutdown", data={}))
        time.sleep(WAIT_TIME)
        # Agent should be stopped
        self.assertFalse(self.mock_agent.running)
        # No messages should have been received
        self.assertEqual(0, len(self.mock_agent.events))

    def test_receives_events(self):
        """The conveyor belts' handle_event method should be called for every event that is posted to it."""
        self.assertEquals([], self.mock_agent.events)
        self.mock_agent.post(Event(type="button", data={}))
        time.sleep(WAIT_TIME)
        self.assertEqual(1, len(self.mock_agent.events))

    @patch("homebrain.base.logging")
    def test_logging_decorators(self, mock_logging):
        """The logging decorators should yield one logging call per event, plus one per exception."""
        self.assertEqual(0, total_debug_calls(mock_logging))
        self.mock_agent.post(Event(type="button", data={}))
        self.mock_agent.post(Event(type="button", data={}))
        self.mock_agent.post(Event(type="button", data={}))
        time.sleep(WAIT_TIME)
        self.assertEqual(3, total_debug_calls(mock_logging))
        self.mock_agent.post(Event(type="test_exception", data={}))
        time.sleep(WAIT_TIME)
        self.assertEqual(5, total_debug_calls(mock_logging))
        self.assertEqual(1, mock_logging.exception.call_count)

    def tearDown(self):
        self.mock_agent.stop()

def total_debug_calls(mock_logging):
    total_debug_calls = mock_logging.debug.call_count +\
                        mock_logging.info.call_count +\
                        mock_logging.warn.call_count +\
                        mock_logging.error.call_count +\
                        mock_logging.exception.call_count +\
                        mock_logging.critical.call_count
    return total_debug_calls
