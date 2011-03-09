from threading import Thread
from socket import *
import struct

DEFAULT_MCAST_PORT = 3141

class NodeInstance(Thread):
    def __init__(self, groupIP, name):
        """Sets up this node instance to listen on the given multicast group
        with a given name.
        
        @type groupIP: string
        @param groupIP: multicast group IP to use for communication with
        control instances.
        
        @type name: string
        @param name: the name of this node."""

        self.groupIP = groupIP
        """Multicast group IP to use for communication with control
        instances."""

        self.name = name
        """The name of this node."""

        self.sock = None
        """A socket connected to the multicast group."""

        self.joinGroup(groupIP)

    def joinGroup(self, port = DEFAULT_MCAST_PORT):
        self.sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind(("", port))

        mreq = struct.pack("=4sl", inet_aton(self.groupIP), INADDR_ANY)
        self.sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)

    def leaveGroup(self):
        mreq = struct.pack("=4sl", inet_aton(self.groupIP), INADDR_ANY)
        self.sock.setsockopt(IPPROTO_IP, IP_DROP_MEMBERSHIP, mreq)
        self.sock.close()

    def run(self):
        while True:
            data = self.sock.recv(10240)