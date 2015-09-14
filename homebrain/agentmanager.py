from datetime import datetime
import logging
from typing import Set, List, Iterable

from . import Agent
from .utils import Singleton

from collections import defaultdict


@Singleton
class AgentManager():
    _agents = []  # type: Set[Agent]
    _subscriptions = defaultdict(list)
    _started = None

    def __init__(self):
        self._started = datetime.now()

    def add_agent(self, agent: Agent):
        if not isinstance(agent, Agent):
            raise Exception("'{}' is not an agent")

        for sub in agent.subscriptions:
            self._subscriptions[sub].append(agent)

        if agent not in self._agents:
            self._agents.append(agent)
        else:
            logging.warning("Agent '{}' already added to the agent manager".format(agent))

    def add_agents(self, agents: List[Agent]):
        for agent in agents:
            self.add_agent(agent)

    @property
    def agents(self) -> Set[Agent]:
        return self._agents

    def get_subscribers(self, type):
        return self._subscriptions[type]

    def _get_by_agent_type(self, agent_type) -> List[Agent]:
        return list(filter(lambda x: x.agent_type == agent_type, self.agents))

    def start_agents(self):
        """Starts loggers first, then filters, then watchers"""
        self._start_agents(self.agents)

    """Starts a list of agents after checking for each of them that they haven't already been started"""
    @staticmethod
    def _start_agents(agents: Iterable[Agent]):
        for agent in agents:
            if not agent.is_alive():
                agent.start()

    def stop_agents(self):
        self._stop_agents(self.loggers)

    def _stop_agents(agents: Iterable[Agent]):
        for agent in agents:
            if agent.is_alive():
                agent.stop()
