from homebrain import Agent, Dispatcher
from homebrain.core.decorators import stop_on_shutdown_event
import logging


import time
import json
import socket
import logging
from socket import *

class BroadcastAgent(Agent):

    autostart = True

    def __init__(self, target=None):
        super(BroadcastAgent, self).__init__()
        self.target = target if target is not None else self.identifier

        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(('', 0))
        self.sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        self.message = json.dumps({ "type": "broadcast",
                                    "data": {
                                        "ip": gethostbyname(gethostname()),
                                        "hostname": gethostname(),
                                        "restport": "5600",
                                        "wsport": "5601",
                                        "udpport": "5602",
                                    }})

    def run(self):
        logging.info("Broadcasting...")
        while True:
            self.sock.sendto(bytes(self.message, 'UTF-8'), ('<broadcast>', 5602))
            time.sleep(15)

    @stop_on_shutdown_event
    def handle_event(self, event):
        # Handle incoming events
        pass
