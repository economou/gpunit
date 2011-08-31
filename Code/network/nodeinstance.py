#!/usr/bin/python

import sys
import struct
from time import sleep

from threading import Thread
from socket import *

import psutil

import network
import threads
import packets
from packets import PacketFactory

# These shouldn't change, so just set them here.
numCPUs = psutil.NUM_CPUS
totalMem = psutil.TOTAL_PHYMEM
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
        control instances

        @type name: string
        @param name: the name of this node"""

        Thread.__init__(self)

        self.groupIP = groupIP
        self.name = name

        self.transmissionThread = threads.TransmissionThread()
        self.receivingThread = threads.ReceivingThread(True, groupIP)
        self.receivingThread.packetHandlers = {
                packets.STATUS_QUERY : self.handleStatusQuery,
                packets.STATUS_RESPONSE : self.handleStatusResponse,
                packets.CAPABILITY_QUERY : self.handleCapabilityQuery,
                packets.CAPABILITY_RESPONSE : self.handleCapabilityResponse,
                }

        self.receivingThread.start()
        self.transmissionThread.start()

    def run(self):
        self.done = False
        while not self.done:
            try:
                sleep(1.0)
            except:
                break
        self.shutdown()
    
    def stop(self):
        self.done = True
        self.join()
    
    def shutdown(self):
        print "Shutting down..."
        self.receivingThread.shutdown()
        self.transmissionThread.shutdown()

        self.receivingThread.join()
        self.transmissionThread.join()

    def handleStatusQuery(self, packet):
        cpuUsage = psutil.cpu_percent()
        usedMem = psutil.used_phymem()
        simsRunning = 0
        
        fields = [str(f) for f in [self.name,cpuUsage,usedMem,simsRunning]]
        response = PacketFactory.packetFromFields(
                packets.STATUS_RESPONSE,
                packet.header.sourceIP,
                fields
        )
        self.transmissionThread.queueData(response)

    def handleStatusResponse(self, packet):
        pass

    def handleCapabilityQuery(self, packet):
        fields = [str(f) for f in [self.name,numCPUs,totalMem,numGPUs]]
        response = PacketFactory.packetFromFields(
                packets.CAPABILITY_RESPONSE,
                packet.header.sourceIP,
                fields
        )
        self.transmissionThread.queueData(response)

    def handleCapabilityResponse(self, packet):
        pass

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: nodeinstance.py MULTICAST_GROUP NODE_NAME"
        sys.exit(1)
    
    ip = sys.argv[1]
    name = sys.argv[2]

    instance = NodeInstance(ip, name)
    instance.start()
    try:
        while True:
            sleep(1.0)
    except KeyboardInterrupt:
        instance.stop()
