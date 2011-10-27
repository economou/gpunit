#!/usr/bin/python

import socket

import threads
import packets

def handleStatusResponse(pkt):
    print "Received status response from",pkt.header.sourceIP
    print "CPU usage:",pkt.usage
    print "Memory usage:",pkt.memoryUsed
    print "Sims running:",pkt.simsRunning
    print

def handleCapabilityResponse(pkt):
    print "Received capability response from",pkt.header.sourceIP
    print "CPUs:",pkt.numCPUs
    print "Memory:",pkt.maxMemory
    print "GPUs:",pkt.numGPUs
    print

trans = threads.TransmissionThread()
recv = threads.ReceivingThread(False)
recv.packetHandlers = {
    packets.STATUS_RESPONSE : handleStatusResponse,
    packets.CAPABILITY_RESPONSE : handleCapabilityResponse,
}
trans.start()
recv.start()

#s = '0|64|%s|224.0.105.200|1' % socket.gethostbyname(socket.getfqdn())
pk = packets.PacketFactory.packetFromFields(packets.CAPABILITY_QUERY,'224.0.105.200',['0'])
trans.queueData(pk)
pk = packets.PacketFactory.packetFromFields(packets.STATUS_QUERY,'224.0.105.200',['0'])
trans.queueData(pk)

print "Press Enter to exit.\n"
raw_input()

print "Shutting down..."
trans.shutdown()
recv.shutdown()
trans.join()
recv.join()
