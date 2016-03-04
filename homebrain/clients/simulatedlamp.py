#!/usr/bin/env python3

from flask import Flask, request
import json
import requests
import socket
import select
import random
app = Flask(__name__)

lamp_state = False

localport = str(int(5610+20*random.random()))

remoteip = None
remoteport = None

def log(msg):
    jsn = json.dumps({"type": "log",
                      "data": {"level": "info", "msg": msg}})
    requests.request("POST", "http://"+remoteip+":"+remoteport+"/api/v0/event", json=jsn)

def add_lamp():
    localip = socket.gethostname()
    jsn = json.dumps({ "type": "add_lamp",
                       "data": { "id": "testlamp", "ip": localip, "port": str(localport)}})
    requests.request("POST", "http://"+remoteip+":"+remoteport+"/api/v0/event", json=jsn)

@app.route("/", methods=["POST"])
def post_event():
    global lamp_state
    event = json.loads(request.json)
    action = event["data"]["action"]

    if action == "toggle":
        lamp_state = not lamp_state
    elif action == "on":
        lamp_state = True
    elif action == "off":
        lamp_state = False

    msg = "Lamp is {}".format("on" if lamp_state else "off")
    print(msg)
    log(msg)
    return ""


def listen_for_homebrain():
    # Set up broadcast listen socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    # Bind socket
    sock.bind(('<broadcast>', 5602))
    # Wait for broadcast message from homebrain server
    homebrain_found = False
    print("Waiting for homebrain server...")
    while not homebrain_found:
        result = select.select([sock],[],[])
        data = result[0][0].recv(4096)
        msg = data.decode('UTF-8')
        if type(msg) is str:
            event = json.loads(msg)
            if event["type"] == "broadcast":
                print("Homebrain server found!")
                global remoteip, remoteport
                remoteip    = event["data"]["ip"]
                remoteport  = event["data"]["restport"]
                add_lamp()
                homebrain_found = True
    sock.close()

if __name__ == '__main__':
    listen_for_homebrain()
    if remoteip and remoteport:
        app.run(host='0.0.0.0', debug=False, port=localport)
    else:
        print("Something went wrong")
