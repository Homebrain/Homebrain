from datetime import datetime
import logging
from typing import Set, List, Iterable

from .core import Agent
from .utils import Singleton

from .modulemanager import ModuleManager

@Singleton
class AgentManager:
    def __init__(self):
        self._agents = set()  # type: Set[Agent]
        self._started = datetime.now()

    def add_agent(self, agent: Agent):
        """
        Adds an agent to be managed

        :param agent: agent to be managed
        """
        if not isinstance(agent, Agent):
            raise Exception("'{}' is not an agent")

        if agent not in self._agents:
            self._agents.add(agent)
        else:
            logging.warning("Agent '{}' already added to the agent manager".format(agent))

    def add_agents(self, agents: List[Agent]):
        """Adds several agents to be managed"""
        for agent in agents:
            self.add_agent(agent)

    @property
    def agents(self) -> Set[Agent]:
        """Contains the set of managed agents"""
        return self._agents

    def start_agents(self):
        """Starts all managed agents not already running, in no particular order."""
        self._start_agents(self.agents)

    @staticmethod
    def _start_agents(agents: Iterable[Agent]):
        """Starts a list of agents after checking for each of them that they haven't already been started"""
        for agent in agents:
            if not agent.is_alive():
                agent.start()

    def stop_agents(self):
        """Stops all agents"""
        self._stop_agents(self.agents)

    @staticmethod
    def _stop_agents(agents: Iterable[Agent]):
        for agent in agents:
            if agent.is_alive():
                agent.stop()
