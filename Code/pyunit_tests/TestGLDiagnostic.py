import os
import unittest
import cPickle
import sys
os.sys.path.append(os.getcwd()+"/..")

from PyQt4.QtGui import QApplication
from diagnostics.builtin.gldiagnostic import OpenGLDiagnostic

class TestOpenGLDiagnostic(unittest.TestCase):
    app = QApplication(sys.argv)

    def setUp(self):
        self.d = OpenGLDiagnostic("gld", 123, 456, 7.0)
    
    def testNeedsGUI(self):
        self.assertTrue(self.d.needsGUI())

    def testNeedsFile(self):
        self.assertFalse(self.d.needsFile())

    def testName(self):
        self.assertEquals(self.d.name, "gld")

    def testWidth(self):
        self.assertEquals(self.d.width, 123)

    def testHeight(self):
        self.assertEquals(self.d.height, 456)

    def testScaleFactor(self):
        self.assertEquals(self.d.scaleFactor, 7.0)

    def testPickle(self):
        tmpfile = open("gltemp.tmp", "w")
        cPickle.dump(self.d, tmpfile)
        tmpfile.close()

        tmpfile = open("gltemp.tmp", "r")
        d = cPickle.load(tmpfile)
        tmpfile.close()

        self.assertTrue(d.needsGUI())
        self.assertFalse(d.needsFile())

        self.assertEquals(self.d.name, d.name)
        self.assertEquals(self.d.width, d.width)
        self.assertEquals(self.d.height, d.height)
        self.assertEquals(self.d.scaleFactor, d.scaleFactor)

    def tearDown(self):
        if os.path.exists("gltemp.tmp"):
            os.remove("gltemp.tmp")
        del self.d

if __name__ == "__main__":
    unittest.main()
