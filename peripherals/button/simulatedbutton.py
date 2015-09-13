import requests
import json

jsn = json.dumps({"type": "button",
    "data":{"wasPressed": False, "isPressed":True}})
requests.request("POST", "http://127.0.0.1:6262/api/v0/event", json=jsn)
