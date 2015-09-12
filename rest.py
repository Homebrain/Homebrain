from flask import Flask, Response, request, json

app = Flask(__name__)

@app.route('/api/0/test')
def test_endpoint():
    data = {"msg": "Hello World!"}
    payload = json.dumps(data)
    r = Response(response=payload,
                 mimetype="application/json")
    return r

if __name__ == '__main__':
    app.run(debug=True)
