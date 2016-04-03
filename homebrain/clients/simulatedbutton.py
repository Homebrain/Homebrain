#!/usr/bin/env python3

import sys, time
import json
from socket import *

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('', 0))
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

print(	"Choose the buttonid:\n"+
		"1: lightbtn0\n"+
		"2: ttsbtn0\n"+
		"3: custom")
choice=input("> ")
eventid=""
if choice=="1":
	eventid="lightbtn0"
elif choice=="2":
	eventid="ttsbtn0"
elif choice=="3":
	eventid=input(">> ")
else:
	print("Invalid choice")
	exit()

data = json.dumps({ "id": eventid,
                    "tag": "button",
                    "data":{"action": "pressed"}})


sock.sendto(bytes(data, 'UTF-8'), ('<broadcast>', 5602))
