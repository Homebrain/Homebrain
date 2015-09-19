#!/usr/bin/env python3

import os
import subprocess

from flask import Flask, request
import json
import requests
app = Flask(__name__)

def say(msg, language="english"):
	print(os.system("espeak -v {} \"{}\"".format(language, msg)))

def isEspeakInstalled():
	out = open("/dev/null")
	statuscode = subprocess.call(["which", "espeak"], stdout=out, stderr=out)
	if statuscode > 0:
		return False
	else:
		return True

def main():
	say("testing")

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
	if isEspeakInstalled():
		app.run(debug=True, port=9092)
	else:
		print("Could not find espeak\n" +
			  "If it is not installed, please install it and if it is installed, please add its directory to your environment variable")
