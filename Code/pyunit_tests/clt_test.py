import os
os.sys.path.append(os.getcwd()+"/..")

import unittest
import exp_management.experiment
from exp_management.experiment import Experiment
import cPickle
class fake_experiment:
    def __init__(self,filename):
        self.filename=filename
    def loadXMLFile(self,*arguments):
        print "test:\t\t",arguments
        

#exp_management.experiment.Experiment = fake_experiment
from exp_gen.CLT import initialization,parse_flags, run_experiment

class CLTTestCase(unittest.TestCase):
    def setup(self):
        self.my_experiment = cPickle.load(open("test/test.exp",'r'))
        print self.my_experiment
        pass
    def test_initialization(self):
        self.setup()
        print self.my_experiment
        pass
    def test_run_experiment(self):
        pass
if __name__=="__main__":
    unittest.main()
