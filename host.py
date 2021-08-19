import serial
import zlib
import os
import random
import json

with open("./hw_desc.json", "r") as f:
    hw_desc = json.load(f)

eoc = 0xABBCCDDE
eof = 0xFFFFFFFF

TIM_FREQ = 80_000_000
desired_freq = 5000
presc = (TIM_FREQ // (2 * desired_freq)) - 1

ser = serial.Serial("/dev/ttyACM1", baudrate=115200, timeout=5)

command = b'\xaa\x65\x6c\x6c\x89\x12'
start = b'\x11'
end = b'\xa0'

crc = zlib.crc32(command).to_bytes(4, byteorder="little")

ser.write(start + command + crc + end)
ser.read_all()


def pack(data):
    crc = zlib.crc32(data).to_bytes(4, byteorder="little")
    return start + data + crc + end


def test(n=10):
    ser.read_all()
    #command = os.urandom(n)
    global data
    data = [random.randint(0, 2**32 - 1) for i in range(n)]
    command = b"".join([d.to_bytes(4, "little") for d in data])
    crc = zlib.crc32(command).to_bytes(4, byteorder="little")

    ser.write(start + command + crc + end)
    resp = ser.read_until(b"\n").decode()
    if "success" in resp:
        return True
    else:
        print(resp)
        return False


ODR = hw_desc['GPIOA']['ODR']['address']

CCER = hw_desc['TIM2']['CCER']['address']
CC3E = 256

ARR = hw_desc['TIM2']['ARR']['address']
presc = presc

CNT = hw_desc['TIM2']['CNT']['address']
cnt_val = 1

CR1 = hw_desc['TIM2']['CR1']['address']
CEN = 1

frames = [(100, CCER, CC3E, ARR, presc, CNT, cnt_val, CR1, CEN, eoc)]

high = (1 << 4)
low = 0

times = [300 + i * 100 for i in range(4000)]
addrs = [ODR] * 4000
vals = [high, low] * 2000

frames = frames + [(t, a, v, eoc) for (t, a, v) in zip(times, addrs, vals)]

frames.append([max(times) + 100, CR1, 0, CCER, 0, eoc])
data_bin = b"".join([item.to_bytes(4, byteorder="little")
                     for sublist in frames for item in sublist])
data_bin += eof.to_bytes(4, byteorder="little")
