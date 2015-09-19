#!/usr/bin/env python3

from flask import Flask, request
import json
import requests
app = Flask(__name__)

lamp_state = False


def log(msg):
    jsn = json.dumps({"type": "log",
                      "data": {"level": "info", "msg": msg}})
    requests.request("POST", "http://127.0.0.1:5000/api/v0/event", json=jsn)


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
    app.run(host='0.0.0.0', debug=True, port=9090)
