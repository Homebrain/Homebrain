from homebrain import Agent, Event
import requests

class LampHandler(Agent):
    """Listens to a trigger event, and sends a toggle command via REST to all registered lamps"""

    def __init__(self, lampurl, target=None):
        super(LampHandler, self).__init__()
        self.target = target if target is not None else self.identifier
        self.lampurl = lampurl

    def handle_event(self, event):
        outgoing_event = Event(type="lamp", data={'action': 'toggle'})
        requests.request("POST", self.lampurl,
                         json=outgoing_event.to_json())
