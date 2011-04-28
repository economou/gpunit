#/usr/bin/python

import sys
import struct
from time import sleep

from threading import Thread
from socket import *

import psutil

import network
import threads
import packet
from packet import PacketFactory

try:
    import pycuda.autoinit
except ImportError:
    numGPUs = 0

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

        self.transmissionThread = threads.TransmissionThread()
        self.receivingThread = threads.ReceivingThread(mcast = True, groupIP)
        self.receivingThread.packetHandlers = {
                packet.STATUS_QUERY : self.handleStatusQuery,
                packet.STATUS_RESPONSE : self.handleStatusResponse,
                packet.CAPABILITY_QUERY : self.handleCapabilityQuery,
                packet.CAPABILITY_RESPONSE : self.handleCapabilityResponse,
                }

        self.receivingThread.start()
        self.transmissionThread.start()

    def run(self):
        self.done = False
        while not self.done:
            try:
                sleep(1.0)
            except:
                print "Shutting down..."
                self.receivingThread.shutdown()
                self.transmissionThread.shutdown()

                self.receivingThread.join()
                self.transmissionThread.join()
                break

    def handleStatusQuery(self, packet):
        cpuUsage = psutil.cpu_percent()
        usedMem = psutil.used_phymem()
        simsRunning = 0

    def handleStatusResponse(self, packet):
        pass

    def handleCapabilityQuery(self, packet):
        numCPUs = psutil.NUM_CPUS
        totalMem = psutil.TOTAL_PHYMEM

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
