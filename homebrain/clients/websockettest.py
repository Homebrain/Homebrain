#!/usr/bin/env python3

import websocket
import json


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print("WSERROR: " + error)


def on_close(ws):
    print("closing")


def on_open(ws):
    msg = {"type": "log", "data": {"level": "info", "msg": "Hello Homebrain! I am a websocket client!"}}
    ws.send(json.dumps(msg))
    msg = {"type": "subscribe", "data": "log"}
    ws.send(json.dumps(msg))
    try:
        while True:
            log_msg = ws.recv()
            print(log_msg)
    except KeyboardInterrupt:
        pass
    ws.close()


if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://127.0.0.1:9091/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
