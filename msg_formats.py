import struct
from fractions import Fraction


# TODO: add robot parameters here
def mmToTicks(mm):
    return mm * 480 / 22


def mmsToSpeed(mms):
    return mms * 67


def input_position(message):
    return [0, 0]


def input_bsensor(message):
    i = struct.unpack(">h", message)
    return struct.pack("!I", i[0])


def arg_bsensor(message):
    return []


def input_sensor(message):
    i = struct.unpack(">h", message)
    return struct.pack("!d", i[0])


def arg_sensor(message):
    return struct.pack(">B", int(message))


def input_twist_busy(message):
    i = struct.unpack(">B", message)
    if i[0] > 0:
        return "b"
    else:
        return "f"


# Repack twist message
def output_twist(message):
    i = struct.unpack("!ddd", message)
    return struct.pack("<hhi", int(mmsToSpeed(i[0])), int(mmsToSpeed(i[1])), int(mmToTicks(i[2])))


# Repack dynamics message
def output_dynamics(message):
    i = struct.unpack("!dd", message)
    acc_fr = Fraction(i[0])
    acc_fr.limit_denominator(32)
    brk_fr = Fraction(i[1])
    brk_fr.limit_denominator(32)
    return struct.pack("<hhhh", acc_fr.numerator, acc_fr.denominator, brk_fr.numerator, brk_fr.denominator)


def output_odetect_limits(message):
    i = struct.unpack("!Ii", message)
    return struct.pack(">hh", i[0], i[1])


def output_servo(message):
    i = struct.unpack("!id", message)
    return struct.pack(">BB", i[0], int(i[1]))


def output_led(message):
    return message


def arg_dummy(message):
    return []

brd_inparse = {
    "position": input_position,
    "bsensor": input_bsensor,
    "sensor": input_sensor,
    "twist_busy": input_twist_busy
}

brd_argparse = {
    "position": arg_dummy,
    "bsensor": arg_dummy,
    "sensor": arg_sensor,
    "twist_busy": arg_dummy
}

brd_outparse = {
    "twist": output_twist,
    "dynamics": output_dynamics,
    "servo": output_servo,
    "odetect_limits": output_odetect_limits,
    "led": output_led,
}
