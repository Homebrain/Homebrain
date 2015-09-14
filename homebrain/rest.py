#!/usr/bin/env python3

from flask import Flask, Response, request, json

app = Flask(__name__, static_url_path='', static_folder='site')

#
#	Static Files
#

@app.route("/")
@app.route("/<_>")
@app.route("/<_>/<__>")
@app.route("/<_>/<__>/<___>")
def index(**_):
	return app.send_static_file("index.html")

@app.route("/scripts/<filename>")
def scripts(filename):
    return app.send_static_file("scripts/" + filename)


@app.route("/templates/<filename>")
def templates(filename):
    return app.send_static_file("templates/" + filename)

#
#	REST API
#

# Static dummy dict
nodes = { 'node1': {'name': 'node1', 'status': 'Hopefully online', 'ip': '192.168.1.3'},
          'node2': {'name': 'node2','status': 'Sadly offline :(', 'ip': '192.168.1.4'}}

@app.route("/api/v0/nodes")
def get_nodes():
    return json.dumps(nodes)

@app.route("/api/v0/nodes/<node_id>")
def get_agent(node_id):
    if node_id in nodes:
        return json.dumps(nodes[node_id])
    else:
        return make_response("Resource not found", 400)

@app.route("/api/v0/agents")
def get_agents():
    agents = { 'agent1': {'status': 'Running'},
               'agent2': {'status': 'Stopped'}}
    return json.dumps(agents)

@app.route('/api/v0/test')
def test_endpoint():
    data = {"msg": "Hello World!"}
    payload = json.dumps(data)
    r = Response(response=payload,
                 mimetype="application/json")
    return r


class DefaultHandler(object):
    def incoming_post(self,data):
        print(request)

agents = {"button": DefaultHandler()}

@app.route("/api/v0/event", methods=["POST"])
def get_event():
    form = json.loads(request.json)
    agents[form["type"]].incoming_post(form["data"])
    return ""

def start_server():
    app.run(debug=True)

if __name__ == '__main__':
    start_server()