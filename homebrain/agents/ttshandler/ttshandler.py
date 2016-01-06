from homebrain import Agent, Event
from homebrain.core.decorators import stop_on_shutdown_event, log_exceptions
import requests

class TTSHandler(Agent):
    """Listens to a trigger event, and sends a toggle command via REST to all registered lamps"""
    def __init__(self, ttsurl, target=None):
        super(TTSHandler, self).__init__()
        self.target = target if target is not None else self.identifier
        self.ttsurl = ttsurl

    @stop_on_shutdown_event
    @log_exceptions
    def handle_event(self, event):
        outgoing_event = Event(type="tts", data={'msg': 'Button pressed'})
        requests.request("POST", self.ttsurl, json=outgoing_event.to_json())
