from datetime import datetime
import logging
from typing import Set, List, Iterable
from collections import defaultdict

from . import Agent
from .utils import Singleton


@Singleton
class AgentManager:
    _agents = set()  # type: set[Agent]
    _started = None

    def __init__(self):
        self._started = datetime.now()

    def add_agent(self, agent: Agent):
        if not isinstance(agent, Agent):
            raise Exception("'{}' is not an agent")

        if agent not in self._agents:
            self._agents.add(agent)
        else:
            logging.warning("Agent '{}' already added to the agent manager".format(agent))

    def add_agents(self, agents: List[Agent]):
        for agent in agents:
            self.add_agent(agent)

    @property
    def agents(self) -> Set[Agent]:
        return self._agents

    def get_subscribers(self, agent_type: str):
        return self._subscriptions[agent_type]

    def start_agents(self):
        """Starts all agents"""
        self._start_agents(self.agents)

    @staticmethod
    def _start_agents(agents: Iterable[Agent]):
        """Starts a list of agents after checking for each of them that they haven't already been started"""
        for agent in agents:
            if not agent.is_alive():
                agent.start()

    def stop_agents(self):
        self._stop_agents(self.loggers)

    @staticmethod
    def _stop_agents(agents: Iterable[Agent]):
        for agent in agents:
            if agent.is_alive():
                agent.stop()
