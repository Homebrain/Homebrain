#!/usr/bin/env python3

import os
import shlex
import subprocess

from flask import Flask, request
import json
import requests
app = Flask(__name__)

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

if __name__ == "__main__":
    if is_espeak_installed():
        app.run(debug=False, port=5603)
    else:
        print("espeak is not installed")
