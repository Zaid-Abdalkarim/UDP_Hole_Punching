#Creator: Zaid Abdalkarim

import logging
import socket
import sys
from util import *
import string
import random
import time

logger = logging.getLogger()
addresses = []

queue = []

hosted_queue = {}

addressLength = 3


def main(host='0.0.0.0', port=25565):
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        pass

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    print("listening on *:%d (udp)" % port)
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print(data.strip())
        logger.info("connection from: %s", addr)
        print(data)

        if data == b'Host':
            letters = string.ascii_letters
            randCode = (''.join(random.choice(letters) for i in range(10)))
            while (hosted_queue.__contains__(randCode)):
                randCode = (''.join(random.choice(letters) for i in range(10)))

            hosted_queue[randCode] = addr_to_msg(addr)
            sock.sendto(string_to_binary(randCode), addr)
        elif data == b'Match':
            addresses.append(addr)
            if len(addresses) >= addressLength:
                i = 0
                for address in addresses[:addressLength + 1]:
                    #safe to assume this will be in there so make adddress 0 the host
                    if i != 0:
                        logger.info("server - send client info to: %s",
                                    addresses[0])
                        sock.sendto(addr_to_msg(address), addresses[0])
                        logger.info("server - send client info to: %s", i)
                        sock.sendto(addr_to_msg(addresses[0]), address)
                    i = i + 1
                i = 0
                while i < addressLength:
                    addresses.pop(0)
                    print(i)
                    i = i + 1
        else:
            key = binary_to_string(
                data
            )  #if they send nothing or something we dont know we pair them with someone who is trying to 'Host'
            sock.sendto(hosted_queue[key], addr)
            sock.sendto(addr_to_msg(addr), msg_to_addr(hosted_queue[key]))
            hosted_queue.pop(key)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main(*addr_from_args(sys.argv))