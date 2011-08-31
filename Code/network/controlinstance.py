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

# ???
class NodeInfo(object):
    def __init__(self,packet = None):
        self.name = ""
        self.numCPUs = 0
        self.maxMemory = 0
        self.numGPUs = 0
        self.usage = 0.0
        self.memoryUsed = 0
        self.simsRunning = 0
        self.hasCapability = False
        #self.haveStatus = False
    
    def __str__(self):
        return \
"""Node: %s
CPUs: %d
GPUs: %d
CPU usage: %.1f%%
Memory usage: %d/%d
Simulations running: %d
""" \
% (self.name, self.numCPUs, self.numGPUs, self.usage, self.memoryUsed, self.maxMemory, self.simsRunning)
        
    def update(self,packet):
        if packet.header.type == packets.CAPABILITY_RESPONSE:
            self.name = packet.name
            self.numCPUs = packet.numCPUs
            self.maxMemory = packet.maxMemory
            self.numGPUs = packet.numGPUs
            self.hasCapability = True
        elif packet.header.type == packets.STATUS_RESPONSE:
            self.name = packet.name
            self.usage = packet.usage
            self.memoryUsed = packet.memoryUsed
            self.simsRunning = packet.simsRunning
            #self.haveStatus = True

class ControlInstance(Thread):
    def __init__(self, groupIP):
        """Sets up this control instance to control NodeInstances on the
        given multicast group.
        
        @type groupIP: string
        @param groupIP: multicast group IP to use for communication with
        node instances."""

        Thread.__init__(self)
        
        self.nodes = {}

        self.groupIP = groupIP
        
        self.transmissionThread = threads.TransmissionThread()
        self.receivingThread = threads.ReceivingThread(False)
        self.receivingThread.packetHandlers = {
                packets.STATUS_RESPONSE : self.handleResponse,
                packets.CAPABILITY_RESPONSE : self.handleResponse,
                }

        self.receivingThread.start()
        self.transmissionThread.start()
        
        self.capabilityQuery = PacketFactory.packetFromFields(packets.CAPABILITY_QUERY,self.groupIP,['0'])
        self.statusQuery = PacketFactory.packetFromFields(packets.STATUS_QUERY,self.groupIP,['0'])

    def run(self):
        self.done = False
        self.transmissionThread.queueData(self.capabilityQuery)
        while not self.done:
            try:
                self.transmissionThread.queueData(self.statusQuery)
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

    def handleResponse(self, packet):
        if packet.name not in self.nodes:
            self.nodes[packet.name] = NodeInfo()
        self.nodes[packet.name].update(packet)
        if not self.nodes[packet.name].hasCapability:
            self.transmissionThread.queueData(self.cababilityQuery)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: controlinstance.py MULTICAST_GROUP"
        sys.exit(1)
    
    ip = sys.argv[1]

    instance = ControlInstance(ip)
    instance.start()
    try:
        while True:
            sleep(1.0)
            print "Status:\n"
            for name in instance.nodes:
                print instance.nodes[name]
            print
    except KeyboardInterrupt:
        instance.stop()
#    instance.join()
