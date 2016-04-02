from homebrain import Agent, Event
import logging
import requests


class ClientAgent(Agent):
    """Listens to a trigger event, and sends a toggle command via REST to all registered lamps"""

    autostart = False

    def __init__(self, name, ip, port, protocol, target=None):
        super(ClientAgent, self).__init__()
        self.target = target if target is not None else self.identifier
        self.ip = ip
        self.port = port
        self.id = name
	# Protocol can either be ws or http at the moment
        self.protocol = protocol

        self.url = protocol + "://" + ip + ":" + port

    def handle_event(self, event):
        if self.protocol == "ws":
            pass
        elif self.protocol == "http":
            pass
        
        try:
            requests.request("POST", self.lampurl,
                             json=event.to_json())
        except Exception as e:
            logging.error("Unable to send event to client: \n" + str(e))

    def send(self, event):
        if self.protocol == "http":
            try:
                requests.request("POST", self.url, json=event)
            except Exception as e:
                logging.error("Unable to send event to client:\n" + str(e))
        elif self.protocol == "ws":
            logging.error("Ws not yet implemented for clientagent")
        else:
            logging.error("Invalid protocol for client")
