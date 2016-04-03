from homebrain import Agent, Event, Dispatcher
from homebrain.core.decorators import stop_on_shutdown_event, log_exceptions
import logging
import requests

class TTSHandler(Agent):
    """Listens to a trigger event, and sends a toggle command via REST to all registered lamps"""

    autostart = False

    def __init__(self, client):
        super(TTSHandler, self).__init__()
        self.client = client

    def handle_event(self, event):
        event["tag"] = "tts"
        event["data"] = {'msg': 'Button pressed'}
        Dispatcher().put_event(event)
