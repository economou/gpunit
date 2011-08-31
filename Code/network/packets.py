import socket

# Field separator.
SEP = "|"

# Number of fields in the header.
HEADER_FIELDS = 4

# Values for packet type in the header.
STATUS_QUERY = 0
STATUS_RESPONSE = 1
CAPABILITY_QUERY = 2
CAPABILITY_RESPONSE = 3

# TODO find a better way
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
sourceIP = s.getsockname()[0]
s.close()
# http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib


class PacketFactory:
    @staticmethod
    def packetFromString(string):
        data = string.split(SEP)
        ptype = int(data[0])
        if ptype in packetTypeDict:
            return packetTypeDict[ptype](string.split(SEP))
        else:
            raise ValueError("Type " + str(ptype) + " is not a valid packet type.")
    
    @staticmethod
    def packetFromFields(ptype,destIP,fields):
        # ???
        length = len(fields)
        #sourceIP = socket.gethostbyname(socket.getfqdn())
        # /???
        data = [ptype,length,sourceIP,destIP] + fields
        if ptype in packetTypeDict:
            return packetTypeDict[ptype](data)
        else:
            raise ValueError("Type " + str(ptype) + " is not a valid packet type.")

class PacketHeader:
    def __init__(self, fields):
        self.type = int(fields[0])
        self.length = long(fields[1])
        self.sourceIP = str(fields[2])
        self.destIP = str(fields[3])

    def __str__(self):
        return SEP.join([str(f) for f in [self.type, self.length, self.sourceIP, self.destIP]])

class Packet:
    def __init__(self, fields):
        self.header = PacketHeader(fields[:HEADER_FIELDS])
        del fields[:HEADER_FIELDS]

    def __str__(self):
        return self.header.__str__()

class StatusQueryPacket(Packet):
    def __init__(self, fields = None):
        if fields is None:
            return
        Packet.__init__(self, fields)
        self.additionalFlags = fields[0]

    def __str__(self):
        return Packet.__str__(self) + SEP + self.additionalFlags

class StatusResponsePacket(Packet):
    def __init__(self, fields = None):
        if fields is None:
            return
        Packet.__init__(self, fields)
        self.name = str(fields[0])
        self.usage = float(fields[1])
        self.memoryUsed = int(fields[2])
        self.simsRunning = int(fields[3])

    def __str__(self):
        return Packet.__str__(self) + SEP + SEP.join(
                [str(f) for f in [self.name, self.usage, self.memoryUsed, self.simsRunning]])

class CapabilityQueryPacket(Packet):
    def __init__(self, fields = None):
        if fields is None:
            return
        Packet.__init__(self, fields)
        self.additionalFlags = fields[0]

    def __str__(self):
        return Packet.__str__(self) + SEP + self.additionalFlags

class CapabilityResponsePacket(Packet):
    def __init__(self, fields = None):
        if fields is None:
            return
        Packet.__init__(self, fields)
        self.name = str(fields[0])
        self.numCPUs = int(fields[1])
        self.maxMemory = int(fields[2])
        self.numGPUs = int(fields[3])

    def __str__(self):
        return Packet.__str__(self) + SEP + SEP.join(
                [str(f) for f in [self.name, self.numCPUs, self.maxMemory, self.numGPUs]])

packetTypeDict = {
    STATUS_QUERY : StatusQueryPacket,
    STATUS_RESPONSE : StatusResponsePacket,
    CAPABILITY_QUERY : CapabilityQueryPacket,
    CAPABILITY_RESPONSE : CapabilityResponsePacket,
}

