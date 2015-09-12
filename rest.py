from flask import Flask, Response, request, json

app = Flask(__name__, static_url_path='', static_folder='./site')

#
#	Static Files
#

@app.route("/")
@app.route("/<_>")
@app.route("/<_>/<__>")
@app.route("/<_>/<__>/<___>")
def index(**_):
	return app.send_static_file("index.html")

@app.route("/scripts/<file>")
def scripts(file):
    return app.send_static_file("scripts/" + file)


@app.route("/templates/<file>")
def templates(file):
    return app.send_static_file("templates/" + file)

#
#	REST API
#

@app.route("/api/v0/nodes")
def get_nodes():
    agents = []
    #return json.dumps(agents)
    return ""

@app.route("/api/v0/agents")
def get_agents():
    agents = {}
    #return json.dumps(agents)
    return ""

@app.route('/api/v0/test')
def test_endpoint():
    data = {"msg": "Hello World!"}
    payload = json.dumps(data)
    r = Response(response=payload,
                 mimetype="application/json")
    return r

if __name__ == '__main__':
    app.run(debug=True)
