import os
os.sys.path.append(os.getcwd()+"/..")
from diagnostics.diagnostic import Diagnostic
import unittest

class CustomDiagnostic(Diagnostic):
    def __init__(self):
        Diagnostic.__init__(self, "CustomTestDiagnostic")
    
    def needsFile(self):
        return True
    
    def needsGUI(self):
        return True


class TestCustomDiagnostic(unittest.TestCase):
    def setUp(self):
        self.d = CustomDiagnostic()
    
    def test_setName(self):
        self.assertEquals(self.d.name, "CustomTestDiagnostic")
        name = "Test_Diagnostic"
        self.d.setName(name)
        self.assertEquals(self.d.name, name)
    
    def test_update(self):
        self.assertRaises(NotImplementedError, self.d.update, None, None, None)
    
    def test_shouldUpdate(self):
        self.assertTrue(self.d.shouldUpdate(None, None))

    def test_needsGUI(self):
        self.assertTrue(self.d.needsGUI())

    def test_setupGUI(self):
        self.assertRaises(NotImplementedError, self.d.setupGUI, None)

    def test_redraw(self):
        self.assertRaises(NotImplementedError, self.d.redraw)

    def test_setupFile(self):
        self.assertRaises(NotImplementedError, self.d.setupFile, "")
    
    def test_needsFile(self):
        self.assertTrue(self.d.needsFile())
        
