#!/usr/bin/env python3

from flask import Flask, request
import json
import socket
import requests
import random
app = Flask(__name__)

import hbcutils

lamp_state = False

localport = str(int(5610+20*random.random()))

def log(msg):
    jsn = json.dumps({"type": "log",
                      "data": {"level": "info", "msg": msg}})
    requests.request("POST", "http://"+remoteip+":"+remoteport+"/api/v0/event", json=jsn)

def add_lamp(remoteip, remoteport):
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

if __name__ == '__main__':
    remoteip, remoteport = hbcutils.listen_for_homebrain()
    if remoteip and remoteport:
        add_lamp(remoteip, remoteport)
        app.run(host='0.0.0.0', debug=False, port=localport)
    else:
        print("Something went wrong")
