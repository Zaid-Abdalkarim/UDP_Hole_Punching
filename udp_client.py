import logging
import socket
import sys
from util import *

logger = logging.getLogger()

connectedto = []

sock = socket.socket(
    socket.AF_INET,  # Internet
    socket.SOCK_DGRAM)  # UDP
sock.bind(('', 0))

data_buffer = 1024  # the size of the message


def main(host='0.0.0.0', port=25565):
    messages = 25
    sock.sendto(b'Match', (host, port))

    while True:
        data, addr = sock.recvfrom(data_buffer)
        print('client received: {} {}'.format(addr, data))
        try:
            if addr_to_msg(addr) == b'127.0.0.1:25565':
                if (msg_to_addr(data)
                    ):  #checks if the content of the message is an address
                    if (
                            not connectedto.__contains__(msg_to_addr(data))
                    ):  # if the server send a person that we dont know we add em' to the list
                        connectedto.append(data)
                        print("we added someone new")
                    sock.sendto(b"Hello", msg_to_addr(
                        data))  # sends a hello message to the new client
                    data, addr = sock.recvfrom(
                        data_buffer)  #recieve message from new client
                    print('client received: {} {}'.format(addr, data))

            print("trying to send" + str(messages) + "messages")

            while messages >= 0:
                for i in connectedto:  #sends a message to everyone that it is connected to EXCEPT the Server
                    if (
                            addr_to_msg(i) != b'127.0.0.1:25565'
                    ):  #Makes sure were not sending a message to the server
                        try:
                            sock.sendto(b"I am testing", msg_to_addr(i))
                            data, addr = sock.recvfrom(data_buffer)
                            print('spam recieved: {} {}'.format(addr, data))
                            if (not connectedto.__contains__(
                                    addr_to_msg(addr)
                            )  # if we recieve a message from someone we dont know we can add em' in the list of addresses
                                    and
                                    addr_to_msg(addr) != b'127.0.0.1:25565'):
                                print("we added someone new")
                                connectedto.append(addr_to_msg(addr))
                            messages = messages - 1
                        except ValueError:
                            print("there was an error sending a message")
        except ValueError:
            print(data)
            raise ValueError


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main(*addr_from_args(sys.argv))
