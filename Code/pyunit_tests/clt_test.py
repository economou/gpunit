#Quick OS Changing and whatnot
import os
os.sys.path.append(os.getcwd()+"/..")
#os.chdir("..")


import mock
import unittest
import exp_management.experiment
from exp_management.experiment import Experiment

#AMUSE Imports
from amuse.support.data.core import Particles
from amuse.support.units import nbody_system
from amuse.support.units import units
#from amuse.support.data.particles import Particles

from diagnostics.builtin.energydiagnostic import EnergyDiagnostic

from exp_management.initialconditions import ParticleDistribution
from exp_management.module import *

from exp_gen.CLT import run_experiment
from amuse.community.hermite0.interface import Hermite

#exp_management.experiment.Experiment = fake_experiment
from exp_gen.CLT import initialization,parse_flags, run_experiment

class sunearth(ParticleDistribution):
    def getParticleList(self):
        p_list = Particles(2)
        p_list[0].position = [0,0,0] | units.km
        p_list[1].position = [1,0,0] | units.AU
        p_list[0].velocity = [0,0,0] | units.km/units.s
        p_list[1].velocity = [0,29.67,0] | units.km/units.s
        p_list.mass = [ 1. , 3.e-6 ] | units.MSun
        p_list.radius = [ 0 , 0 ] | units.km
        return p_list

class CLTTestCase(unittest.TestCase):
    def setup(self):
        my_experiment = Experiment()
        my_experiment.initialConditions.append(sunearth('2'))
#        my_experiment.initialConditions[sunearth('2')]='2'
        my_experiment.diagnostics.append(EnergyDiagnostic())#'energylogger'
#        my_experiment.diagnostics.append()#]='visual python viewer'
        my_experiment.modules.append(Module.fromFile("../exp_management/Modules_XML/hermite0.xml"))

        self.my_experiment = my_experiment #cPickle.load(open("test/test.exp",'r'))
    def test_initialization(self):
        self.setup()
        modules,particles,convert_nbody = initialization(self.my_experiment)
        self.assertTrue(len(modules) > 0, "Module list is too small")
        self.assertTrue(isinstance(modules[0],Hermite),"Module is suppose to be Hermite type Module")
        self.assertTrue(None == modules[0].evolve_model(1|units.s), "Evolve model returns bad stuff")
        self.assertTrue(isinstance(particles,Particles),"Particles are suppose to be Particles type class")
#        self.assertTrue(isinstance(convert_nbody
        print dir(self)
       
       # self.assertTrue(
        
    def test_run_experiment(self):
        pass
if __name__=="__main__":
    unittest.main()
