from homebrain import Agent, Dispatcher
from homebrain.core.decorators import stop_on_shutdown_event
import logging

class AgentTemplate(Agent):

    autostart = False

    def __init__(self):
        super(AgentTemplate, self).__init__()

        # Only bind manually if you are an endpoint agent. Otherwise, use Dispatcher.chain at config time.
        #Dispatcher().bind(self, "exampletype1")

    @stop_on_shutdown_event
    def handle_event(self, event):
        # Handle incoming events
        pass
