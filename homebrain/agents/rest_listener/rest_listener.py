#!/usr/bin/env python3
from homebrain import AgentManager, ModuleManager, Agent, Dispatcher
from homebrain.utils import *
from flask import Flask, Response, request, json, make_response


# PROPOSAL: Make a core component (not an agent) with a separate agent that
#           hooks the core component allowing for communication via an API
#           endpoint such as /api/v0/endpoint/<name>/<method>.
#           Such an agent should be able to have multiple instances running,
#           for different purposes.

# TODO: Change to a better name

class RestListener(Agent):
    def __init__(self):
        super(RestListener, self).__init__()
        self.dispatcher = Dispatcher()
        self.app = Flask(__name__, static_url_path='', static_folder=get_cwd() + '/site')

        #
        #    EVENT API
        #
        @self.app.route("/api/v0/event", methods=["POST"])
        def post_event():
            msg = request.json
            if type(msg) is str:
                event = json.loads(msg)
            else:
                event = msg
            self.dispatcher.put_event(event)
            return ""

        #
        #   HTTP Static Files
        #

        @self.app.route("/")
        @self.app.route("/<_>")
        @self.app.route("/<_>/<__>")
        @self.app.route("/<_>/<__>/<___>")
        def index(**_):
            return self.app.send_static_file("index.html")

        @self.app.route("/styles/<filename>")
        def styles(filename):
            return self.app.send_static_file("styles/" + filename)

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
        nodes = {'node1': {'name': 'dummynode1', 'status': True, 'ip': '192.168.1.3'},
                 'node2': {'name': 'dummynode2', 'status': False, 'ip': '192.168.1.4'}}

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
            agents = {}
            for agent in AgentManager().agents:
                agents[agent.identifier] = agent.to_json_dict()
            return json.dumps(agents)

        @self.app.route('/api/v0/modules')
        def get_modules():
            modules = {}
            for module in ModuleManager().modules:
                modules[module.agentclass.__name__] = {
                    "name": module.agentclass.__name__,
                    "autostart": module.autostart }
            return json.dumps(modules)

    def run(self):
        self.app.run(host='0.0.0.0', port=20444, debug=False)

    def stop(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
