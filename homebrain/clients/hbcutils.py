"""

Homebrain Controller Utilities
##############################

A collection of helper functions for homebrain clients written in python

"""

import socket
import select
import json

def listen_for_homebrain():
    # Set up broadcast listen socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    # Bind socket
    sock.bind(('<broadcast>', 5602))
    # Wait for broadcast message from homebrain server
    homebrain_found = False
    print("Waiting for homebrain server...")
    while not homebrain_found:
        result = select.select([sock],[],[])
        data = result[0][0].recv(4096)
        msg = data.decode('UTF-8')
        if type(msg) is str:
            event = json.loads(msg)
            if event["type"] == "broadcast":
                print("Homebrain server found!")
                global remoteip, remoteport
                remoteip    = event["data"]["ip"]
                remoteport  = event["data"]["restport"]
                homebrain_found = True
    sock.close()
    return remoteip, remoteport
