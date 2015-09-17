
from homebrain import Agent, Dispatcher, Event
from websocket_server import WebsocketServer
import threading
import json

class WebSocket(Agent):
    def __init__(self):
        super(WebSocket, self).__init__()
        self.server = WebsocketServer(9091)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.clients = self.server.clients
        self.subscriptions = []

    def run(self):
        self.wsthread = threading.Thread(target=self.server.run_forever)
        self.wsthread.start()
        self.listener()

    def listener(self):
        while self.wsthread.isAlive():
            event = self.next_event()
            etype = event["type"]
            data = event["data"]
            for client in self.clients:
                if etype in client["subscriptions"]:
                    self.server.send_message(client, json.dumps(event))

    def new_client(self, client, server):
        client["subscriptions"] = []

    def client_left(self, client, server):
        print("Client(%d) disconnected" % client['id'])

    def message_received(self, client, server, msg):
        #print("Client{}: {}".format(client['id'], msg))
        event = json.loads(msg)
        etype = event["type"]
        data  = event["data"]
        if etype == "subscribe":
            client["subscriptions"].append(str(data))
            if not str(data) in self.subscriptions:
                self.subscriptions.append(str(data))
                Dispatcher().bind(self, data)
            print("Client subscribed to " + data)
        elif etype == "unsubscribe":
            if str(data) in client["subscriptions"]:
                client["subscriptions"].remove(data)
                othersubscriber = False
                for otherclient in self.clients:
                    if str(data) in otherclient["subscriptions"]:
                        othersubscriber = True
                if not othersubscriber:
                    self.subscriptions.remove(str(data))
                print("Client unsubscribed from " + data)
        else:
            Dispatcher().post(Event(type=etype, data=data))
