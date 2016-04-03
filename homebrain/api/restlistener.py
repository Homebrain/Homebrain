#!/usr/bin/env python3
import logging
from homebrain import AgentManager, ModuleManager, Agent, Dispatcher
from homebrain.utils import *
import threading
import flask
from flask import Flask, Response, request, json, make_response

# PROPOSAL: Make a core component (not an agent) with a separate agent that
#           hooks the core component allowing for communication via an API
#           endpoint such as /api/v0/endpoint/<name>/<method>.
#           Such an agent should be able to have multiple instances running,
#           for different purposes.

# TODO: Change to a better name

class RestListener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        from devicemonitor import DeviceMonitor
        self.dispatcher = Dispatcher()
        self.app = Flask(__name__, static_url_path='', static_folder=get_cwd() + '/site')

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

        # Agent specific static files
        @self.app.route("/agent/<agent>/<filename>")
        def agentfile(agent, filename):
            agentfolder = filelocation = get_cwd()+"/agents/"+agent.lower()+"/site/"
            return flask.send_from_directory(agentfolder, filename)

        #
        #	WEB API
        #

        # TODO: Rename resource to devices
        @self.app.route("/api/v0/nodes")
        def get_nodes():
            devicemonitor = None
            for agent in AgentManager().agents:
                if agent.__class__.__name__ is DeviceMonitor.__name__:
                    devicemonitor = agent
            if not devicemonitor or not devicemonitor.enabled:
                return make_response("DeviceMonitor is not running, cannot fetch nodes", 500)
            else:
                return json.dumps(devicemonitor.known_devices)

        @self.app.route("/api/v0/nodes/<node_id>")
        def get_agent(node_id):
            devicemonitor = None
            for agent in AgentManager().agents:
                if agent.__class__.__name__ is DeviceMonitor.__name__:
                    devicemonitor = agent
            if not devicemonitor or not devicemonitor.enabled:
                return make_response("DeviceMonitor is not running, cannot fetch nodes", 500)
            else:
                devices = devicemonitor.known_devices
                if node_id in devices:
                    return json.dumps(devices[node_id])
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
                modules[module.__name__] = {
                    "name": module.__name__,
                    "autostart": module.autostart}
            return json.dumps(modules)

        @self.app.route('/api/v0/chains')
        def get_chains():
            chains = list(Dispatcher()._chains)
            jchains = []
            for chain in chains:
                arr = []
                print(chain)
                for agent in chain:
                    print(agent)
                    arr.append(agent.identifier)
                jchains.append(arr)
            retval = {"chains":jchains}
            print(retval)
            return json.dumps(retval)

        """EVENT API"""

        @self.app.route("/api/v0/event", methods=["POST"])
        def post_event():
            msg = request.json
            if type(msg) is str:
                event = json.loads(msg)
            else:
                event = msg
            self.dispatcher.put_event(event)
            return ""

    def run(self):
        self.app.run(host='0.0.0.0', port=5600, debug=False)

    def stop(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
