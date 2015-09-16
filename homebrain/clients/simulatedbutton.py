#!/usr/bin/env python3

import requests
import json

jsn = json.dumps({"type": "button",
    "data":{"action": "pressed"}})
requests.request("POST", "http://127.0.0.1:5000/api/v0/event", json=jsn)
