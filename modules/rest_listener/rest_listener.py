#!/usr/bin/env python3
import threading
from flask import Flask, Response, request, json


class RestListener(threading.Thread):

    def __init__(self, dispatcher):
        super(RestListener, self).__init__()
        self.dispatcher=dispatcher
        self.app = Flask(__name__, static_url_path='')

        @self.app.route("/api/v0/event", methods=["POST"])
        def post_event():
            event = json.loads(request.json)
            self.dispatcher.post(event)
            return ""

    def run(self):
        self.app.run(debug=False, port=6262)

if __name__=="__main__":
    RestListener()
