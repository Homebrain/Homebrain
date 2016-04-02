from homebrain import Agent, Event
from homebrain.core.decorators import stop_on_shutdown_event, log_exceptions
import logging
import requests

class TTSHandler(Agent):
    """Listens to a trigger event, and sends a toggle command via REST to all registered lamps"""

    autostart = False

    def __init__(self, client, target=None):
        super(TTSHandler, self).__init__()
        self.target = target if target is not None else self.identifier
        self.client = client

    def handle_event(self, event):
        outgoing_event = Event(tag="tts", data={'msg': 'Button pressed'})
        self.client.send(outgoing_event)
