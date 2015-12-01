
from homebrain import Agent, Dispatcher, Event
from websocket_server import WebsocketServer
import threading
import logging
import json


class WebSocket(Agent):
    def __init__(self):
        super(WebSocket, self).__init__()
        self.server = WebsocketServer(20445)
        self.wsThread = threading.Thread(target=self.server.run_forever)
        self.clients = self.server.clients
        self.subscriptions = []

        @self.server.set_fn_new_client
        def new_client(client, server):
            client["subscriptions"] = []

        @self.server.set_fn_client_left
        def client_left(client, server):
            logging.info("Client(%d) disconnected" % client['id'])

        @self.server.set_fn_message_received
        def message_received(client, server, msg):
            event = json.loads(msg)
            event_type = event["type"]
            event_data = event["data"]
            if event_type == "subscribe":
                self._subscribe(client, event_data)
            elif event_type == "unsubscribe":
                self._unsubscribe(client, msg)
            else:
                Dispatcher().put_event(Event(type=event_type, data=event_data))

    def run(self):
        self.wsThread.start()
        self._listener()

    def _listener(self):
        while self.wsThread.isAlive():
            event = self.next_event()
            event_type = event["type"]
            event_data = event["data"]
            for client in self.clients:
                if event_type in client["subscriptions"]:
                    self.server.send_message(client, json.dumps(event))

    def _subscribe(self, client, event_data):
        client["subscriptions"].append(str(event_data))
        if not str(event_data) in self.subscriptions:
            self.subscriptions.append(str(event_data))
            Dispatcher().bind(self, event_data)
        logging.info("Client subscribed to " + event_data)

    def _unsubscribe(self, client, event_data):
        if str(event_data) in client["subscriptions"]:
            client["subscriptions"].remove(event_data)
            othersubscriber = False
            for otherclient in self.clients:
                if str(event_data) in otherclient["subscriptions"]:
                    othersubscriber = True
            if not othersubscriber:
                self.subscriptions.remove(str(event_data))
            logging.info("Client unsubscribed from " + event_data)
        else:
            # Client wasn't found in subscribers list
            pass
