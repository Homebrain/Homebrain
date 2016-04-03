
from homebrain import Agent, Dispatcher, Event, AgentManager
from websocket_server import WebsocketServer
import threading
import logging
import json

from homebrain.utils import Singleton



@Singleton
class WebSocket(threading.Thread):

    autostart = True

    def __init__(self):
        # This import is needed here because the modulemanager needs to load it first
        from homebrain.agents.clientagent import ClientAgent

        threading.Thread.__init__(self)
        self.server = WebsocketServer(5601, "0.0.0.0")
        self.clients = self.server.clients

        @self.server.set_fn_new_client
        def new_client(client, server):
            # TODO: Fix name
            name = "noname websocket"
            ip = client["address"][0]
            port = str(client["address"][1])
            client["agent"] = ClientAgent(name, ip, port, "ws")
            AgentManager().add_agent(client["agent"])
            AgentManager().start_agents()

        @self.server.set_fn_client_left
        def client_left(client, server):
            logging.info("Client(%d) disconnected" % client['id'])

        @self.server.set_fn_message_received
        def message_received(client, server, msg):
            if msg:
                try:
                    event = json.loads(msg)
                    event_tag = event["tag"]
                    event_data = event["data"]
                    if event_tag == "subscribe" or event_tag ==  "unsubscribe":
                        # TODO: This is very hackish and not modular
                        event_data["agent"] = client["agent"].id
                    Dispatcher().put_event(Event(tag=event_tag, data=event_data))
                except json.decoder.JSONDecodeError as e:
                    pass


    def send(self, ip, port, event):
        client = self._get_client_by_ipport(ip, port)
        if client is not None:
            self.server.send_message(client, json.dumps(event))

    def _get_client_by_ipport(self, ip, port):
        target = None
        for client in self.clients:
            address = client["address"]
            if address[0] == ip and address[1] == int(port):
                target = client
        return target


    def run(self):
        self.server.run_forever()
