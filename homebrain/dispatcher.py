import logging
from collections import defaultdict

from .utils import Singleton
from .agentmanager import AgentManager
from .base import Agent


@Singleton
class Dispatcher(Agent):
    def __init__(self):
        Agent.__init__(self)
        self._bindings = defaultdict(set)
        self.daemon = False

    def run(self):
        while True:
            self.process(self.next_event())

    def bind(self, agent, selector):
        self._bindings[selector].add(agent)

    def _query_selector(self, selector):
        """Returns all the agents that match the selector"""
        return self._bindings[selector]

    def process(self, msg):
        agents = self._query_selector(msg["type"])
        for agent in agents:
            agent.post(msg)

    def chain(self, initial_trigger, *args):
        """Chains together a sequence of agents such that each one listens to the preceding one's event,
        and outputs an event the following agent will listen to."""
        trigger = initial_trigger
        for agent in args:
            self.bind(agent, trigger)
            trigger = "{}->{}".format(trigger, agent)
            agent.target = trigger
        AgentManager().add_agents(args)
