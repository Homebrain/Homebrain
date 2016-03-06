from homebrain import Agent, Event
import logging
import requests

class LampHandler(Agent):
    """Listens to a trigger event, and sends a toggle command via REST to all registered lamps"""

    autostart = False

    def __init__(self, lampid, lampurl, target=None):
        super(LampHandler, self).__init__()
        self.target = target if target is not None else self.identifier
        self.id = lampid
        self.lampurl = lampurl

    def handle_event(self, event):
        outgoing_event = Event(type="lamp", data={'action': 'toggle'})
        try:
            requests.request("POST", self.lampurl,
                             json=outgoing_event.to_json())
        except Exception as e:
            logging.error("Unable to send lampevent to lamp:\n" + str(e))
