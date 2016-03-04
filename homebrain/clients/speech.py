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


localport = str(int(5610+20*random.random()))

remoteip = None
remoteport = None


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
    jsn = json.dumps({ "type": "add_tts",
                       "data": { "id": "ttsclient", "ip": localip, "port": str(localport)}})
    requests.request("POST", "http://"+remoteip+":"+remoteport+"/api/v0/event", json=jsn)

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
                add_tts()
                homebrain_found = True
    sock.close()

if __name__ == "__main__":
    if not is_espeak_installed():
        print("espeak is not installed")
    else:
        listen_for_homebrain()
        if remoteip and remoteport:
            app.run(host='0.0.0.0', debug=False, port=localport)
