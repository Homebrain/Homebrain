import unittest
import threading
import time

from homebrain import Agent, AgentManager, Dispatcher, Event
from homebrain.agents.chunker.chunker import Chunker
from homebrain.agents.idfilter.idfilter import IDFilter
#from homebrain.agents.lamphandler.lamphandler import LampHandler

from queue import Queue, Empty


class MockOutputter(Agent):
    def run(self):
        self.events = []
        while self.running:
            try:
                event = self.next_event(timeout=0.01)
                self.events.append(event)
            except Empty as e:
                pass

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        AgentManager()
        Dispatcher()
        Dispatcher().daemon = True
        Dispatcher().start()
        self.output_agent = MockOutputter()
        Dispatcher().chain("button" , Chunker(3), self.output_agent)
        Dispatcher().chain("button", IDFilter("idtest"), self.output_agent)
        AgentManager().start_agents()
        time.sleep(0.1)

    def test_chain(self):
        # Test Chunker
        self.assertEquals([],self.output_agent.events)
        Dispatcher().put_event(Event(type="button", data={}))
        self.assertEquals([],self.output_agent.events)
        Dispatcher().put_event(Event(type="button", data={}))
        Dispatcher().put_event(Event(type="button", data={}))
        time.sleep(0.1)
        self.assertEqual(1, len(self.output_agent.events))

        # Test IDFilter
        Dispatcher().put_event(Event(type="button", id="", data={}))
        time.sleep(0.1)
        self.assertEqual(1, len(self.output_agent.events))
        Dispatcher().put_event(Event(type="button", id="idtest", data={}))
        time.sleep(0.1)
        self.assertEqual(2, len(self.output_agent.events))

    def tearDown(self):
        AgentManager.reset_singleton()
        Dispatcher.reset_singleton()
        self.output_agent.stop()
