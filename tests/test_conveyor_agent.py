from homebrain import ConveyorAgent, Event, Dispatcher
from homebrain import Agent, AgentManager, Dispatcher, Event
import unittest
import threading
import time

WAIT_TIME = 0.02  # time to sleep while waiting for a thread to react


class MockConveyor(ConveyorAgent):
    def __init__(self):
        super(MockConveyor, self).__init__()
        self.events = []

    @ConveyorAgent.stop_on_shutdown_event
    @ConveyorAgent.log_events
    def handle_event(self, event):
        self.events.append(event)

    def cleanup(self):
        pass


class ConveyorAgentTest(unittest.TestCase):
    def setUp(self):
        self.mock_agent = MockConveyor()
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

    def tearDown(self):
        self.mock_agent.stop()
