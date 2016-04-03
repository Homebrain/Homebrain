from homebrain import Agent, Event, Dispatcher, AgentManager

import logging

class DispatchInterface(Agent):
    """Listens to a certain trigger event, and emits a target event once the specified count has been reached."""

    autostart = True

    def __init__(self):
        Agent.__init__(self)
        self.dispatcher = Dispatcher()
        Dispatcher().bind(self, "subscribe")
        Dispatcher().bind(self, "unsubscribe")

    def handle_event(self, event):
        tag = event["tag"]
        data = event["data"]

        if tag == "subscribe":
            agent = AgentManager().get_agent(data["agent"])
            subtag = data["tag"]
            if agent is None:
                logging.warning("Tried to subscribe, but there's no agent named "+data["agent"])
            elif subtag is None:
                logging.warning("Tried to subscribe, but no tag was specified "+data["agent"])
            else:
                self.dispatcher.bind(agent, subtag)
                logging.info(agent.identifier+" subscribed to "+subtag)
        
        elif tag == "unsubscribe":
            agent = AgentManager().get_agent(data["agent"])
            subtag = data["tag"]
            if agent is None:
                logging.warning("Tried to unsubscribe, but there's no agent named "+data["agent"])
            elif subtag is None:
                logging.warning("Tried to unsubscribe, but no tag was specified "+data["agent"])
            else:
                # TODO: Create unbind in dispatcher and add it here
                #self.dispatcher.bind(agent, subtag)
                logging.info(agent.identifier+" unsubscribed from "+subtag)
