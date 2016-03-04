from homebrain import Agent, Event, Dispatcher
from homebrain.core.decorators import stop_on_shutdown_event, log_exceptions
import logging

import json
import select, socket

class UDPListener(Agent):
    """Listens to a trigger event, and sends a toggle command via REST to all registered lamps"""
    def __init__(self, target=None):
        super(UDPListener, self).__init__()
        self.target = target if target is not None else self.identifier
        self.port = 5602
        self.bufsize = 4096
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        self.socket.bind(('<broadcast>', self.port))
        while True:
            result = select.select([self.socket],[],[])
            data = result[0][0].recv(self.bufsize)
            msg = data.decode('UTF-8')

            if type(msg) is str:
                event = json.loads(msg)
            else:
                event = msg
            if event["type"] != "broadcast":
                Dispatcher().put_event(event)
