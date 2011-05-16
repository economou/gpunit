import os
os.sys.path.append(os.getcwd()+"/..")
from diagnostics.diagnostic import Diagnostic
import unittest

class TestDiagnostic(unittest.TestCase):
    def setUp(self):
        self.d = Diagnostic()
    
    def test_setName(self):
        self.assertEquals(self.d.name, "BaseDiagnostic")
        name = "Test_Diagnostic"
        self.d.setName(name)
        self.assertEquals(self.d.name, name)
        self.d.setName("BaseDiagnostic")
    
    def test_update(self):
        self.assertRaises(NotImplementedError, self.d.update, None, None, None)
    
    def test_shouldUpdate(self):
        self.assertTrue(self.d.shouldUpdate(None, None))

    def test_needsGUI(self):
        self.assertFalse(self.d.needsGUI())
    
    def test_needsFile(self):
        self.assertFalse(self.d.needsFile())
        
