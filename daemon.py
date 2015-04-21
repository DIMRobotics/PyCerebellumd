#!/usr/bin/env python

from pycerebellumd import socket, board_rq

while True:
    msg = socket.recv_multipart()
    reply = board_rq(msg)
    if reply[0] == "BAD":
        print "Bad request"
    socket.send_multipart(reply)
