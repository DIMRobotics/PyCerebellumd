#!/usr/bin/env python

from pycerebellumd import socket, board_rq

while True:
    msg = socket.recv_multipart()
    reply = board_rq(msg)
    socket.send_multipart(reply)
