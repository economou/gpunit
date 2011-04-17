#/usr/bin/python

import sys
import struct

from threading import Thread
from socket import *

import packet
from packet import PacketFactory

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

        Thread.__init__(self)

        self.groupIP = groupIP
        """Multicast group IP to use for communication with control
        instances."""

        self.name = name
        """The name of this node."""

        self.sock = None
        """A socket connected to the multicast group."""

        self.packetHandlers = {
                packet.STATUS_QUERY : self.handleStatusQuery,
                packet.STATUS_RESPONSE : self.handleStatusResponse,
                packet.CAPABILITY_QUERY : self.handleCapabilityQuery,
                packet.CAPABILITY_RESPONSE : self.handleCapabilityResponse,
                }

        self.joinGroup()

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
            data = str(self.sock.recv(10240))
            packet = PacketFactory.packetFromString(data)
            self.packetHandlers[packet.header.type](packet)

    def handleStatusQuery(self, packet):
        print "Got StatusQueryPacket:", packet
        self.leaveGroup()
        exit(0)

    def handleStatusResponse(self, packet):
        pass

    def handleCapabilityQuery(self, packet):
        pass

    def handleCapabilityResponse(self, packet):
        pass

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: nodeinstance MULTICAST_GROUP NODE_NAME"
        sys.exit(1)
    
    ip = sys.argv[1]
    name = sys.argv[2]

    instance = NodeInstance(ip, name)
    instance.start()
    instance.join()
