import unittest
import threading

from homebrain import Agent, AgentManager, Dispatcher, Event


class MockAgent(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.event_received = threading.Event()

    def create_event(self):
        Dispatcher().put_event(Event(**{"type": "test"}))

    def run(self):
        event = self.next_event()
        self.event_received.set()


class DispatcherTest(unittest.TestCase):
    def setUp(self):
        self.am = AgentManager()
        self.dispatcher = Dispatcher()
        self.dispatcher.daemon = True
        self.dispatcher.start()

    def test_subscription(self):
        agent = MockAgent()
        self.am.add_agent(agent)
        self.dispatcher.bind(agent, "test")

        agent.create_event()
        agent.start()

        timed_out = not agent.event_received.wait(1)
        if timed_out:
            self.fail("Event not received")

    def tearDown(self):
        AgentManager.reset_singleton()
        Dispatcher.reset_singleton()
