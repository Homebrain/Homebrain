import unittest
import threading
import time

from homebrain import Agent, AgentManager, Dispatcher, Event
from homebrain.agents.chunker.chunker import Chunker
from homebrain.agents.lamphandler.lamphandler import LampHandler

from queue import Queue, Empty

class MockOutputter(Agent):
    def run(self):
        self.running = True
        self.events = []
        while self.running:
            try:
                event = self.next_event(timeout=0.01)
                self.events.append(event)
            except Empty as e:
                pass
    def stop(self):
        self.running = False

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        AgentManager()
        Dispatcher()
        Dispatcher().daemon = True
        Dispatcher().start()
        self.output_agent = MockOutputter()
        Dispatcher().chain("button" , Chunker(3), self.output_agent)
        AgentManager().start_agents()
        time.sleep(0.1)

    def test_chain(self):
        self.assertEquals([],self.output_agent.events)
        Dispatcher().post(Event(type="button", data={}))
        self.assertEquals([],self.output_agent.events)
        Dispatcher().post(Event(type="button", data={}))
        Dispatcher().post(Event(type="button", data={}))
        time.sleep(0.1)
        self.assertEqual(1, len(self.output_agent.events))

    def tearDown(self):
        AgentManager.reset_singleton()
        Dispatcher.reset_singleton()
        self.output_agent.stop()


