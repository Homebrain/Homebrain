from homebrain import Agent, Event
import requests

class TTSClient:
    def __init__(self, name, url):
        self.name = name
        self.url = url

class TTSHandler(Agent):
    """Listens to a trigger event, and sends a toggle command via REST to all registered lamps"""
    def __init__(self, host, target=None):
        super(TTSHandler, self).__init__()
        self.target = target if target is not None else self.identifier
        self.clients = []
        self.host = host

    def add_client(self, url, name=None):
        if name == None:
            name = "Unnamed Lamp"
        self.clients.append(TTSClient(name, url))

    def run(self):
        while True:
            event = self.next_event()
            outgoing_event = Event(type="tts", data={'msg': 'Button pressed'})
            requests.request("POST", self.host, json=outgoing_event.to_json_str())
