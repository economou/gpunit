import logging
import sys
import struct

from threading import Thread, Condition
from socket import *

import network

class ReceivingThread(Thread):
    def __init__(self, mcast, groupIP = "", port = network.DEFAULT_GPUNIT_PORT):
        Thread.__init__(self)

        self.port = port
        self.isMcastThread = mcast

        self.doneCond = Condition()
        self.packetHandlers = {}
        self.groupIP = groupIP

        if self.isMcastThread:
            self.joinGroup()

    def joinGroup(self):
        self.socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(("", self.port))

        mreq = struct.pack("=4sl", inet_aton(self.groupIP), INADDR_ANY)
        self.socket.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)

    def leaveGroup(self):
        mreq = struct.pack("=4sl", inet_aton(self.groupIP), INADDR_ANY)
        self.socket.setsockopt(IPPROTO_IP, IP_DROP_MEMBERSHIP, mreq)
        self.socket.close()

    def run(self):
        self.done = False
        while not self.done:
            data = str(self.socket.recv(10240))
            packet = PacketFactory.packetFromString(data)
            if packet.header.type in self.packetHandlers:
                self.packetHandlers[packet.header.type](packet)

    def shutdown(self):
        self.doneCond.acquire()
        self.done = True
        self.doneCond.wait(2.0)

        self.socket.shutdown()
        self.socket.close()


class TransmissionThread(Thread):
    def __init__(self, port = network.DEFAULT_GPUNIT_PORT):
        Thread.__init__(self)

        self.log = logging.getLogger("TransmissionThreadLogger")
        # TODO: Remove the next two lines for release, let the user configure
        # this.
        self.log.setLevel(logging.INFO)
        self.log.addHandler(logging.StreamHandler())

        self.socket = socket()
        self.port = port
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(("", self.port))

        self.queueCond = Condition()
        self.doneCond = Condition()
        self.packetQueue = []

    def run(self):
        self.done = False

        while not self.done:
            self.queueCond.acquire()
            self.queueCond.wait(1.0)
            while len(self.packetQueue) > 0:
                packet = self.packetQueue.pop()
                destIP = packet.header.destIP
                self.sock.sendto(str(packet), (destIP, network.DEFAULT_GPUNIT_PORT))
                self.log.info("Sent packet: ", str(packet))

            self.doneCond.acquire()
            self.doneCond.notifyAll()

    def shutdown(self):
        self.doneCond.acquire()
        self.done = True
        self.doneCond.wait(2.0)

        self.socket.shutdown()
        self.socket.close()

    def queueData(self, packet):
        self.queueCond.acquire()

        self.packetQueue.insert(0, packet)

        self.queueCond.notifyAll()
        self.queueCond.release()
