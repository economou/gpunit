from amuse.support.data.core import Particles
from amuse.support.units import nbody_system
from amuse.support.units import units

from diagnostics.Diagnostic_scripts.EnergyLogging import EnergyLogger

from exp_management.Experiment import Experiment

from exp_management.initialconditions import ParticleDistribution
from exp_management.Module import Module
from exp_gen.CLT import run_experiment
from amuse.community.hermite0.interface import Hermite
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
if __name__ == '__main__':
    my_experiment = Experiment()
    my_experiment.initialConditions[sunearth('2')]='2'
    my_experiment.diagnostics[EnergyLogger()]='energylogger'

    module_str = '\n'.join(open('exp_management/Modules_XML/hermite0.xml','r').readlines())
#    print module_str
    my_experiment.modules.append(Module.fromXML(module_str))
#    gravity=Hermite()
    run_experiment(my_experiment)
#    my_experiment.
#    my_experiment.particles = Particles(2)
#    my_experiment.particles[0].position = [0,0,0] | units.km
#    my_experiment.particles[1].position = [1,0,0] | units.AU
#    my_experiment.particles[0].velocity = [0,0,0] | units.km/units.s
#    my_experiment.particles[1].velocity = [0,29.67,0] | units.km/units.s
#    my_experiment.particles.mass = [ 1. , 3.e-6 ] | units.MSun
    
    
