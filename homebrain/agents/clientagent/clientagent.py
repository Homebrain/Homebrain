from homebrain import Agent, Event, AgentManager
import logging
import requests
from homebrain.api import WebSocket

class ClientAgent(Agent):
    """Listens to a trigger event, and sends a toggle command via REST to all registered lamps"""

    autostart = False

    def __init__(self, name, ip, port, protocol):
        super(ClientAgent, self).__init__()
        self.ip = ip
        self.port = port
        self.id = name
	# Protocol can either be ws or http at the moment
        self.protocol = protocol

        self.url = protocol + "://" + ip + ":" + port

    def handle_event(self, event):
        self.send(event)

    def send(self, event):
        if self.protocol == "http":
            try:
                requests.request("POST", self.url, json=event)
            except Exception as e:
                logging.error("Unable to send event to client:\n" + str(e))
        elif self.protocol == "ws":
            ws = WebSocket()
            ws.send(self.ip, self.port, event)
        else:
            logging.error("Invalid protocol for client")
