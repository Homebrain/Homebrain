from homebrain import Agent, Event, Dispatcher
import logging
import requests

class LampHandler(Agent):
    """Listens to a trigger event, and sends a toggle command via REST to all registered lamps"""

    autostart = False

    def __init__(self, lamp):
        super(LampHandler, self).__init__()
        self.client = lamp

    def handle_event(self, event):
        event["tag"] = "lamp"
        event["data"] = {'action': 'toggle'}
        Dispatcher().put_event(event)
