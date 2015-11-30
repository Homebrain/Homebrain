from homebrain import Agent, Event
import requests


class Lamp:
    def __init__(self, name, url):
        self.name = name
        self.url = url


class LampHandler(Agent):
    """Listens to a trigger event, and sends a toggle command via REST to all registered lamps"""

    def __init__(self, target=None):
        super(LampHandler, self).__init__()
        self.target = target if target is not None else self.identifier
        self.lamps = []
        self.add_lamp("http://localhost:9090/", "Simulated lamp")

    def add_lamp(self, url, name=None):
        if name is None:
            name = "Unnamed Lamp"
        self.lamps.append(Lamp(name, url))

    def handle_event(self, event):
        outgoing_event = Event(type="lamp", data={'action': 'toggle'})
        for lamp in self.lamps:  # Toggle all lamps
            requests.request("POST", lamp.url,
                             json=outgoing_event.to_json())
