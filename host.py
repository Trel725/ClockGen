import serial
import zlib
import os
ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=5)

command = b'\xaa\x65\x6c\x6c\x89\x12'
start = b'\x11'
end = b'\xa0'

crc = zlib.crc32(command).to_bytes(4, byteorder="little")

ser.write(start + command + crc + end)
ser.read_all()


def test(n=10):
    ser.read_all()
    command = os.urandom(n)
    crc = zlib.crc32(command).to_bytes(4, byteorder="little")

    ser.write(start + command + crc + end)
    resp = ser.read_until(b"\n").decode()
    if "success" in resp:
        return True
    else:
        print(resp)
        return False
