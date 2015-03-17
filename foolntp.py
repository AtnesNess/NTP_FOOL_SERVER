import socket
import struct
from decimal import Decimal
import argparse
import threading
NTP_HEADER_LENGTH = 48
COUNT_TIME = 0.0016
NTP_HEADER_FORMAT = ">BBBBII4sQQQQ"
NTP_UTC_OFFSET = 2208988800

TEMPLATE = (36, 2, 0, 238, 3602, 2077,
            b'\xc1\xbe\xe6A', 0, 0, 0, 0)


def reply(server, data, addr, shift):
    shift = Decimal((2 ** 32)*shift)
    res = struct.unpack(NTP_HEADER_FORMAT, data)
    tmp = TEMPLATE
    origin_time = res[-1]
    new_data = struct.pack(NTP_HEADER_FORMAT, tmp[0], tmp[1],
                           tmp[2], tmp[3], tmp[4],
                           tmp[5], tmp[6],  int(origin_time-shift), int(origin_time+shift*2),
                           int(origin_time),
                           int(origin_time))
    server.sendto(new_data, addr)
    # time.sleep(10) # if you need to check threading


def main(shift):
    shift = float(shift)

    print("shift is {}sec".format(shift))
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("", 43))

    while True:
        data, addr = server.recvfrom(512)
        t = threading.Thread(target=reply, args=(server, data, addr, shift))
        t.start()
    server.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NTP FOOL SERVER")
    parser.add_argument("shift", help="shift in ms")
    args = parser.parse_args()
    shift = args.shift
    main(shift)