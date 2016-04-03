import logging
import copy
from collections import defaultdict

from .utils import Singleton
from .agentmanager import AgentManager
from .core import Agent

class Chain(list):
    # A list of agents
    def __init__(self, tag):
        self.starttag = tag
        self = []


@Singleton
class Dispatcher(Agent):
    def __init__(self):
        Agent.__init__(self)
        self._bindings = defaultdict(set)
        self._chains = []

    def run(self):
        while True:
            self.process(self.next_event())

    def bind(self, agent, selector):
        self._bindings[selector].add(agent)

    def _query_selector(self, selector):
        """Returns all the agents that match the selector"""
        return self._bindings[selector]

    def process(self, msg):
        if "type" not in msg:
            # Default behavior is broadcast
            msg["type"] = "broadcast"

        print(msg)
        if msg["type"] != "chain":
            for ci in range(len(self._chains)):
                chain = self._chains[ci]
                if chain.starttag == msg["tag"]:
                    cmsg = copy.copy(msg)
                    cmsg["type"] = "chain"
                    cmsg["chain"] = { "pos": 0, "index":ci }
                    cagent = chain[0]
                    cagent.put_event(cmsg)

        if msg["type"] == "unicast":
            logging.warning("Unicast is not tested yet, proceed with caution!")
            agent = AgentManager().get_agent(msg["agent"])
            agent.put_event(msg)
        
        elif msg["type"] == "chain":
            chainpos = msg["chain"]["pos"]
            chain = self._chains[msg["chain"]["index"]]
            agent = chain[chainpos]
            msg["chain"]["pos"] = chainpos + 1
            agent.put_event(msg)

        elif msg["type"] == "broadcast":
            agents = self._query_selector(msg["tag"])
            for agent in agents:
                agent.put_event(msg)


    def chain(self, initial_trigger, *args):
        """Chains together a sequence of agents such that each one listens to the preceding one's event,
        and outputs an event to the next agent one in the chain if any."""
        # TODO: Needs better documentation
        chain = Chain(initial_trigger)
        trigger = initial_trigger
        for agent in args:
            chain.append(agent)
        
        print("Created chain "+str(chain))
        print("start trigger:" + chain.starttag)
        self._chains.append(chain)
        AgentManager().add_agents(args)
