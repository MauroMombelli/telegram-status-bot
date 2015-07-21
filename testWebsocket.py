#!/usr/bin/python

#shameless copypaste from http://stackoverflow.com/questions/3142705/is-there-a-websocket-client-implemented-for-python

from websocket import create_connection
ws = create_connection("ws://ws.pusherapp.com")
print ("Sending 'Hello, World'...")
ws.send("Hello, World")
print ("Sent")
print ("Reeiving...")
result =  ws.recv()
print ("Received '%s'" % result)
ws.close()
