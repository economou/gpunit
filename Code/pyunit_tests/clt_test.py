#Quick OS Changing and whatnot
import os
os.sys.path.append(os.getcwd()+"/..")

#os.chdir("..")

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
        my_experiment.startTime = 0   | units.day
        my_experiment.timeStep  = 1   | units.day
        my_experiment.stopTime  = 365 | units.day

        self.my_experiment = my_experiment #cPickle.load(open("test/test.exp",'r'))
    def test_initialization_modules(self):
        self.setup()
        modules,particles,convert_nbody = initialization(self.my_experiment)
        self.assertTrue(len(modules) > 0, "Module list is too small")
        self.assertTrue(isinstance(modules[0],Hermite),"Module is suppose to be Hermite type Module")
        self.assertTrue(None == modules[0].evolve_model(1|units.s), "Evolve model returns bad stuff")
    def test_initialization_particles(self):
        self.setup()
        modules,particles,convert_nbody = initialization(self.my_experiment)
        self.assertTrue(isinstance(particles,Particles),"Particles are suppose to be Particles type class")
        self.assertTrue(len(particles) == 2,"Their is a wrong number of Particles")
    def test_initialization_conversion(self):
        self.setup()
        modules,particles,convert_nbody = initialization(self.my_experiment)
        self.assertTrue(isinstance(convert_nbody,nbody_system.nbody_to_si),"Convert Nbody is Wrong Class Type")
        self.assertTrue(abs(convert_nbody.to_si(1|nbody_system.length).value_in(units.parsec) - 1.0) < 1e-7,
            "Testing that the conversion Converts length correct")
        self.assertTrue(abs(convert_nbody.to_si(1|nbody_system.mass).value_in(units.MSun) - 1000.0) < 1e-7,
            "Testing that the conversion Converts mass correct")
    def test_run_experiment(self):
        self.setup()
        self.my_experiment.diagnostics[-1].fout=open("Testfile",'w')
        time, dt, tmax, modules, loggers, diagnostics, particles = run_experiment(self.my_experiment)
        self.my_experiment.diagnostics[-1].fout.close()
        print time, dt, tmax, modules, loggers, diagnostics, particles
        
        self.assertTrue(isinstance(particles,Particles),"Particles are suppose to be Particles type class")
        self.assertTrue(len(particles) == 2,"Their is a wrong number of Particles")

        self.assertTrue(sum(((particles[1].position - ([1,0,0]|units.AU)).value_in(units.AU))**2 ) < 1e-2,
            "Earth returns back to initial location")
        self.assertTrue(sum(((particles[0].position - ([0,0,0]|units.AU)).value_in(units.AU))**2 ) < 1e-2,
            "Sun Remains in initial location")
        self.assertTrue( 0 |time.unit <= time-tmax < dt, "End time is in correct range")

        self.assertTrue(len(modules) > 0, "Module list is too small")
        self.assertTrue(isinstance(modules[0],Hermite),"Module is suppose to be Hermite type Module")
        
        checkfile=open("Testfile",'r').readlines()
        os.remove("Testfile")
        self.assertTrue(len(checkfile)/2 - tmax/dt == 1., "Data file read in not right length from Energy Diagnostic")
        
        
        
        pass
if __name__=="__main__":
    unittest.main()
