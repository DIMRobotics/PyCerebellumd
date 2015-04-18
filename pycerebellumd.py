import serial as s
import struct
import zmq
from msg_formats import brd_inparse, brd_outparse, brd_argparse
from sys import argv

brd_inregs = {
    "twist_busy": 6,
    "bsensor": 2,
    "sensor": 3,
}

brd_outregs = {
    "twist": 1,
    "dynamics": 2,
    "servo": 3,
    "odetect_limits": 4,
    "led": 5
}


# initialize ZMQ socket for external communication
zcontext = zmq.Context()
socket = zcontext.socket(zmq.REP)
socket.bind("tcp://*:1234")

# initialize serial port for board communication
serial = s.Serial(argv[1], baudrate=230400, timeout=1.0)


# functions for communication with board
def board_rq(msg):
    # 1. select message method
    if msg[0] == "get":
        if not brd_inregs.has_key(msg[1]):
            return ["BAD"]

        return brd_read(msg[1], msg[2])

    elif msg[0] == "set":
        if not brd_outregs.has_key(msg[1]):
            return ["BAD"]

        return brd_write(msg[1], msg[2])

    else:
        return ["BAD"]


def recv_reply():
    ln = serial.read()
    ln = struct.unpack(">B", ln)[0]
    print ln

    reply = ""

    while ln > 0:
        ch = serial.read()
        reply += ch
        ln -= 1

    return reply


def brd_read(msg_type, data):
    # accept arguments data
    data = brd_argparse[msg_type](data)
    rq = struct.pack(">BB", brd_inregs[msg_type], len(data))

    # send to client
    serial.write("g")  # get
    serial.write(rq)
    serial.write(data)

    # get reply
    reply = recv_reply()

    return brd_inparse[msg_type](reply)


def brd_write(msg_type, value):
    # accept data
    data = brd_outparse[msg_type](value)
    rq = struct.pack(">BB", brd_outregs[msg_type], len(data))

    # send it to client
    serial.write("s")  # set
    serial.write(rq)
    serial.write(data)

    # wait for reply
    reply = serial.read()

    if reply == 'y':
        return ["OK"]
    else:
        return ["BAD"]
