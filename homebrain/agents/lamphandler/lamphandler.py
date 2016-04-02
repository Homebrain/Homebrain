from homebrain import Agent, Event
import logging
import requests

class LampHandler(Agent):
    """Listens to a trigger event, and sends a toggle command via REST to all registered lamps"""

    autostart = False

    def __init__(self, lamp, target=None):
        super(LampHandler, self).__init__()
        self.target = target if target is not None else self.identifier
        self.client = lamp

    def handle_event(self, event):
        outgoing_event = Event(tag="lamp", data={'action': 'toggle'})
        self.client.send(outgoing_event)
