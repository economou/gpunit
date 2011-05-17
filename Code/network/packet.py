# Field separator.
SEP = "|"

# Number of fields in the header.
HEADER_FIELDS = 4

# Values for packet type in the header.
STATUS_QUERY = 0
STATUS_RESPONSE = 1
CAPABILITY_QUERY = 2
CAPABILITY_RESPONSE = 3

class PacketFactory:
    @staticmethod
    def packetFromString(string):
        type = int(string.split("|")[0])
        if type == STATUS_QUERY:
            return StatusQueryPacket(string)
        if type == STATUS_RESPONSE:
            return StatusResponsePacket(string)
        if type == CAPABILITY_QUERY:
            return CapabilityQueryPacket(string)
        if type == CAPABILITY_RESPONSE:
            return CapabilityResponsePacket(string)
        else:
            raise ValueError("Type " + str(type) + " is not a valid packet type.")

class PacketHeader:
    def __init__(self, fields):
        self.type = int(fields[0])
        self.length = long(fields[1])
        self.sourceIp = str(fields[2])
        self.destIP = str(fields[3])

    def __str__(self):
        return SEP.join([str(f) for f in [self.type, self.length, self.sourceIp, self.destIP]])

class Packet:
    def __init__(self, fields):
        self.header = PacketHeader(fields[:HEADER_FIELDS])
        del fields[:HEADER_FIELDS]

    def __str__(self):
        return self.header.__str__()

class StatusQueryPacket(Packet):
    def __init__(self, data = None):
        if data is None:
            return

        fields = data.split("|")
        Packet.__init__(self, fields)

        self.additionalFlags = fields[0]

    def __str__(self):
        return Packet.__str__(self) + SEP + self.additionalFlags

class StatusResponsePacket(Packet):
    def __init__(self, data = None):
        if data is None:
            return

        fields = data.split("|")
        Packet.__init__(self, fields)

        self.usage = float(fields[0])
        self.memoryUsed = int(fields[1])
        self.simsRunning = int(fields[2])

    def __str__(self):
        return Packet.__str__(self) + SEP + SEP.join(
                [str(f) for f in [self.usage, self.memoryUsed, self.simsRunning]])

class CapabilityQueryPacket(Packet):
    def __init__(self, data = None):
        if data is None:
            return

        fields = data.split("|")
        Packet.__init__(self, fields)

        self.additionalFlags = fields[0]

    def __str__(self):
        return Packet.__str__(self) + SEP + self.additionalFlags

class CapabilityResponsePacket(Packet):
    def __init__(self, data = None):
        if data is None:
            return

        fields = data.split("|")
        Packet.__init__(self, fields)

        self.numCPUs = int(fields[0])
        self.maxMemory = int(fields[1])
        self.numGPUs = int(fields[2])

    def __str__(self):
        return Packet.__str__(self) + SEP + SEP.join(
                [str(f) for f in [self.numCPUs, self.maxMemory, self.numGPUs]])
