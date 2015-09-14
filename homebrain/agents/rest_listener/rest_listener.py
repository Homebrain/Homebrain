#!/usr/bin/env python3
import threading
from flask import Flask, Response, request, json

class RestListener(threading.Thread):

    def __init__(self, dispatcher):
        super(RestListener, self).__init__()
        self.dispatcher=dispatcher
        self.app = Flask(__name__, static_url_path='', static_folder=get_cwd()+'/site')


        @self.app.route("/")
        @self.app.route("/<_>")
        @self.app.route("/<_>/<__>")
        @self.app.route("/<_>/<__>/<___>")
        def index(**_):
            return self.app.send_static_file("index.html")

        @self.app.route("/scripts/<filename>")
        def scripts(filename):
            return self.app.send_static_file("scripts/" + filename)


        @self.app.route("/templates/<filename>")
        def templates(filename):
            return self.app.send_static_file("templates/" + filename)

        #
        #	WEB API
        #

        # Static dummy dict
        nodes = { 'node1': {'name': 'node1', 'status': 'Hopefully online', 'ip': '192.168.1.3'},
                'node2': {'name': 'node2','status': 'Sadly offline :(', 'ip': '192.168.1.4'}}

        @self.app.route("/api/v0/nodes")
        def get_nodes():
            return json.dumps(nodes)

        @self.app.route("/api/v0/nodes/<node_id>")
        def get_agent(node_id):
            if node_id in nodes:
                return json.dumps(nodes[node_id])
            else:
                return make_response("Resource not found", 400)

        @self.app.route("/api/v0/agents")
        def get_agents():
            agents = { 'agent1': {'status': 'Running'},
                    'agent2': {'status': 'Stopped'}}
            return json.dumps(agents)

        @self.app.route('/api/v0/test')
        def test_endpoint():
            data = {"msg": "Hello World!"}
            payload = json.dumps(data)
            r = Response(response=payload,
                        mimetype="application/json")
            return r


        #
        #    EVENT API
        #
        @self.app.route("/api/v0/event", methods=["POST"])
        def post_event():
            event = json.loads(request.json)
            self.dispatcher.post(event)
            return ""

    def run(self):
        self.app.run(debug=False)
