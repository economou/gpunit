import os
import unittest

os.sys.path.append(os.getcwd()+"/..")

from network.packet import *

class TestPackets(unittest.TestCase):
    def setUp(self):
        pass

    def testFactoryStatusQuery(self):
        p = PacketFactory.packetFromString("0|5|localhost|localhost|FLAGS")
        self.assertTrue(isinstance(p, StatusQueryPacket))

    def testFactoryStatusResponse(self):
        p = PacketFactory.packetFromString("1|7|localhost|localhost|0|0|0")
        self.assertTrue(isinstance(p, StatusResponsePacket))

    def testFactoryCapabilityQuery(self):
        p = PacketFactory.packetFromString("2|5|localhost|localhost|FLAGS")
        self.assertTrue(isinstance(p, CapabilityQueryPacket))

    def testFactoryCapabilityResponse(self):
        p = PacketFactory.packetFromString("3|7|localhost|localhost|0|0|0")
        self.assertTrue(isinstance(p, CapabilityResponsePacket))

    def testHeaderStr(self):
        h = PacketHeader(["3", "4", "localhost", "localhost"])

        self.assertEquals(h.type, 3)
        self.assertEquals(h.length, 4)
        self.assertEquals(h.sourceIp, "localhost")
        self.assertEquals(h.destIP, "localhost")

        self.assertEquals(str(h), "3|4|localhost|localhost")

    def testStatusQueryStr(self):
        p = StatusQueryPacket("0|5|localhost|localhost|FLAGS")
        self.assertEquals(str(p), "0|5|localhost|localhost|FLAGS")

    def testStatusResponseStr(self):
        p = StatusResponsePacket("1|7|localhost|localhost|0|0|0")
        self.assertEquals(str(p), "1|7|localhost|localhost|0.0|0|0")

    def testCapabilityQueryStr(self):
        p = CapabilityQueryPacket("2|5|localhost|localhost|FLAGS")
        self.assertEquals(str(p), "2|5|localhost|localhost|FLAGS")

    def testCapabilityResponseStr(self):
        p = CapabilityResponsePacket("3|7|localhost|localhost|0|0|0")
        self.assertEquals(str(p), "3|7|localhost|localhost|0|0|0")

if __name__ == "__main__":
    unittest.main()
