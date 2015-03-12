import socket
import struct
from decimal import Decimal
import argparse
import time
NTP_HEADER_LENGTH = 48
COUNT_TIME = 0.0016
NTP_HEADER_FORMAT = ">BBBBII4sQQQQ"
NTP_UTC_OFFSET = 2208988800
TEMPLATE = (36, 2, 0, 238, 3602, 2077,
            b'\xc1\xbe\xe6A', 0, 0, 0, 0)


def main(shift):
    shift = float(shift)
    print("shift is {}ms".format(shift))
    shift *= 0.001
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("", 43))

    while True:
        data, addr = server.recvfrom(512)
        res = struct.unpack(NTP_HEADER_FORMAT, data)
        tmp = TEMPLATE
        origin_time = res[-1]
        receive_time = Decimal((2 ** 32)*(time.time()+NTP_UTC_OFFSET))
        trip_delay = receive_time - origin_time
        send_time = Decimal((2 ** 32)*(time.time()+COUNT_TIME+NTP_UTC_OFFSET-shift))
        new_data = struct.pack(NTP_HEADER_FORMAT, tmp[0], tmp[1],
                               tmp[2], tmp[3], tmp[4],
                               tmp[5], tmp[6], tmp[7], int(origin_time), int(receive_time), int(send_time-trip_delay))
        server.sendto(new_data, addr)
    server.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NTP FOOL SERVER")
    parser.add_argument("shift", help="shift in ms")
    args = parser.parse_args()
    shift = args.shift
    main(shift)