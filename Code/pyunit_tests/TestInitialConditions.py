import os
import unittest
import sys
import cPickle

os.sys.path.append(os.getcwd()+"/..")

from PyQt4.QtGui import QApplication
from exp_management.initialconditions import *

class TestPlummerModel(unittest.TestCase):
    app = QApplication(sys.argv)

    def setUp(self):
        self.i = PlummerModel(51)

    def testPickle(self):
        tmpfile = open("inittemp.tmp", "w")
        cPickle.dump(self.i, tmpfile)
        tmpfile.close()

        tmpfile = open("inittemp.tmp", "r")
        i = cPickle.load(tmpfile)
        tmpfile.close()

        self.assertEquals(self.i.name, i.name)
        self.assertEquals(self.i.numParticles, i.numParticles)
        self.assertEquals(self.i.convert_nbody, i.convert_nbody)
        self.assertEquals(self.i.radius_cutoff, i.radius_cutoff)
        self.assertEquals(self.i.mass_cutoff, i.mass_cutoff)
        self.assertEquals(self.i.do_scale, i.do_scale)
        self.assertEquals(self.i.random_state, i.random_state)

    def tearDown(self):
        if os.path.exists("inittemp.tmp"):
            os.remove("inittemp.tmp")
        del self.i

class TestSalpeterModel(unittest.TestCase):
    app = QApplication(sys.argv)

    def setUp(self):
        self.i = SalpeterModel(51)

    def testPickle(self):
        tmpfile = open("inittemp.tmp", "w")
        cPickle.dump(self.i, tmpfile)
        tmpfile.close()

        tmpfile = open("inittemp.tmp", "r")
        i = cPickle.load(tmpfile)
        tmpfile.close()

        self.assertEquals(self.i.name, i.name)
        self.assertEquals(self.i.numParticles, i.numParticles)
        self.assertEquals(self.i.mass_min, i.mass_min)
        self.assertEquals(self.i.mass_max, i.mass_max)
        self.assertEquals(self.i.alpha, i.alpha)

    def tearDown(self):
        if os.path.exists("inittemp.tmp"):
            os.remove("inittemp.tmp")
        del self.i

class TestKingModel(unittest.TestCase):
    app = QApplication(sys.argv)

    def setUp(self):
        self.i = KingModel(51)

    def testPickle(self):
        tmpfile = open("inittemp.tmp", "w")
        cPickle.dump(self.i, tmpfile)
        tmpfile.close()

        tmpfile = open("inittemp.tmp", "r")
        i = cPickle.load(tmpfile)
        tmpfile.close()

        self.assertEquals(self.i.name, i.name)
        self.assertEquals(self.i.numParticles, i.numParticles)
        self.assertEquals(self.i.W0, i.W0)
        self.assertEquals(self.i.convert_nbody, i.convert_nbody)
        self.assertEquals(self.i.do_scale, i.do_scale)
        self.assertEquals(self.i.beta, i.beta)
        self.assertEquals(self.i.seed, i.seed)
        self.assertEquals(self.i.verbose, i.verbose)

    def tearDown(self):
        if os.path.exists("inittemp.tmp"):
            os.remove("inittemp.tmp")
        del self.i

if __name__ == "__main__":
    unittest.main()
