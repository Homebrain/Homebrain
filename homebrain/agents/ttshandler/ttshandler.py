from homebrain import Agent, Event
from homebrain.core.decorators import stop_on_shutdown_event, log_exceptions
import logging
import requests

class TTSHandler(Agent):
    """Listens to a trigger event, and sends a toggle command via REST to all registered lamps"""

    autostart = False

    def __init__(self, ttsid, ttsurl, target=None):
        super(TTSHandler, self).__init__()
        self.target = target if target is not None else self.identifier
        self.ttsurl = ttsurl
        self.id = ttsid

    @stop_on_shutdown_event
    @log_exceptions
    def handle_event(self, event):
        outgoing_event = Event(type="tts", data={'msg': 'Button pressed'})
        try:
            requests.request("POST", self.ttsurl, json=outgoing_event.to_json())
        except Exception as e:
            logging.error("Unable to send ttsevent to ttsnode:\n" + str(e))
