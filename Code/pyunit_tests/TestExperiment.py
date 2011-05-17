import os
os.sys.path.append(os.getcwd()+"/..")
from exp_management.experiment import Experiment
from diagnostics.diagnostic import Diagnostic
from loggers.logger import Logger
import unittest

class TestExperiment(unittest.TestCase):
    def setUp(self):
        self.ex = Experiment("TestExperiment")
        self.ex.stopIsEnabled = False
        self.diag = Diagnostic("TestDiag")
        self.ex.addDiagnostic(self.diag)
        self.logg = Logger("TestLogger")
        self.ex.addLogger(self.logg)
        self.ex.scaleToStandard = True
    
    def test_copy(self):
        self.assertEquals(self.ex.name, "TestExperiment")
        newExp = self.ex.copy()
        self.assertEquals(self.ex.name, newExp.name)
        self.assertEquals(self.ex.stopIsEnabled,newExp.stopIsEnabled)
        self.assertEquals(self.ex.scaleToStandard,newExp.scaleToStandard)
        self.assertEquals(self.ex.loggers[0],newExp.loggers[0])
        self.assertEquals(self.ex.diagnostics[0],newExp.diagnostics[0])
        self.assertEquals(self.timeUnit,newExp.timeUnit)
        self.assertEquals(self.startTime,newExp.startTime)
        self.assertEquals(self.stopTime,newExp.stopTime)
        self.assertEquals(self.timeStep,newExp.timeStep)

if __name__=="__main__":
    unittest.main()
        
