#!/usr/bin/env python3

import os
import shlex
import subprocess
import random
import socket
import select

from flask import Flask, request
import json
import requests
app = Flask(__name__)

import hbcutils


localport = str(int(5610+20*random.random()))

ERROR_MSG_ESPEAK_MISSING = """Could not find espeak
Or please install it or if it is already installed, please add its directory to your environment variable"""

def say(msg, language="english"):
    print("Saying: " + msg)
    command = shlex.split("espeak -v {} \"{}\"".format(language, msg))
    subprocess.Popen(command)


def is_espeak_installed():
    out = open("/dev/null")
    statuscode = subprocess.call(["which", "espeak"], stdout=out, stderr=out)
    if statuscode > 0:
        return False
    else:
        return True


@app.route("/", methods=["POST"])
def post_event():
    event = json.loads(request.json)
    data = event["data"]
    print(data)
    # Language
    language = "english"
    if "language" in data:
        language = data["language"]
    # Msg
    msg = event["data"]["msg"]
    # Talk
    say(msg, language)
    return ""

def add_tts():
    localip = socket.gethostname()
    jsn = json.dumps({ "tag": "add_client",
        "data": { "ip": localip, "port": str(localport), "protocol": "http", "tags": ["tts"]}})
    requests.request("POST", "http://"+remoteip+":"+remoteport+"/api/v0/event", json=jsn)

if __name__ == "__main__":
    if not is_espeak_installed():
        print("espeak is not installed")
    else:
        remoteip, remoteport = hbcutils.listen_for_homebrain()
        if remoteip and remoteport:
            add_tts()
            app.run(host='0.0.0.0', debug=False, port=localport)
