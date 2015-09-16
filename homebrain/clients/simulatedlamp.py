#!/usr/bin/env python3

from flask import Flask, request
import json
app = Flask(__name__)

lamp_state = False

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

    print("Lamp is {}".format("on" if lamp_state else "off"))
    return ""

if __name__ == '__main__':
    app.run(debug=True, port=9090)
