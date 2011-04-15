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
        self.destIp = str(fields[3])

class Packet:
    def __init__(self, fields):
        self.header = PacketHeader(fields[:HEADER_FIELDS])
        del fields[:HEADER_FIELDS]

class StatusQueryPacket(Packet):
    def __init__(self, data):
        fields = data.split("|")

        Packet.__init__(self, fields)

        self.additionalFlags = fields[0]

class StatusResponsePacket(Packet):
    def __init__(self, data):
        fields = data.split("|")
        Packet.__init__(self, fields)

class CapabilityQueryPacket(Packet):
    def __init__(self, data):
        fields = data.split("|")
        Packet.__init__(self, fields)

        self.additionalFlags = fields[0]

class CapabilityResponsePacket(Packet):
    def __init__(self, fields):
        fields = data.split("|")
        Packet.__init__(self, fields)
