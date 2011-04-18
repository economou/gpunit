#!/usr/bin/python
#
# CLT.py
#    The CLT is used for running of an experiment file for
#    an AMUSE simulation.
#
# Tim McJilton
# 2/11
#
# Team GPUnit - Senior Design 2011
#
#

from exp_management.Experiment import Experiment

from amuse.support.units import nbody_system
from amuse.support.units import units 
from exp_management.initialconditions import MassDistribution, ParticleDistribution
def parse_flags():
    import getopt
    import sys
    experiment = Experiment("EXP1")

    #Check for Help Flag
    if(sys.argv.count("--help")):
        sys.exit(0)
    #Make sure there is a filename passed in using a flag
    if(not sys.argv.count("-f")):
        sys.stderr.write("Must pass in filename using -f <filename>\n")
        sys.exit(1)

    #Get all pairing of options to args
    try:
        opts,args = getopt.getopt(sys.argv[1:],"f:n:t:d:r")
    except getopt.GetoptError,err:
        print str(err)
        sys.exit(1)
    
    experiment.loadXMLFile( filter(lambda x:x[0] == '-f',opts)[-1][1] )
    for (flag,value) in filter(lambda x:x[0] <> '-f',opts):
        print flag,value
        if flag == '-n':
            pass #Experiment needs the ability to have a number of particles for init conditions#            experiment.set
        elif flag == '-t':
            #experiment.setEndTime(float(opts))
            pass #Need something for setting end time
        elif flag == '-d':
            experiment.setTimeStep(float(value))
        elif flag == '-r':
            pass
            #experiment.setRadius(float(value))
    print experiment.getTimeStep()


    
    return experiment
#class ModuleRunner:
#	def __init__(self, p_experiment):
#		self.experiment = p_experiment
#		self.dt   = self.experiment.getTimeStep()
#		self.time = 0 | self.experiment.timeUnit

def initialization(experiment):
    '''
       Takes in an experiment object, parses the initialization.
       Take the initialization to initialize and return:
            modules:       Actual objects ready to  use for evolve_model
            particles:     AMUSE Particles class of all particles
            convert_nbody: Used for converting between nbody units and regular units
    '''
    r    = 1 | units.parsec #Placeholder till we do this right.
    
    particle_sets = []
    last_set = None
    #Loop through all Initial Conditions
    for ic in experiment.initialConditions:
        #If Initial Conditionis Mass Distribution set last set to have this mass
        if isinstance(ic, MassDistribution):
            last_set = MassDistribution
            particle_sets[-1].mass = ic.getScaledMass()
        #If Inititial Conditions is Particle Distribution append the new Particles object
        else:
            last_set = ParticleDistribution
            particle_sets.append(ic.getParticleList())
    
    #union all of the Particles sets together
    if len(particle_sets)-1:
        for p in particle_sets[1:]:
            particle_sets[0].add_particles(p)
    particles = particle_sets[0] 
        
    #Get Modules actual class values
    modules = [mod.result for mod in experiment.modules]
    
    #Total mass used for conversion object
#    total_mass = reduce(lambda x,y:x+y, particles.mass)
    
    #Create Conversion Object
#    convert_nbody = nbody_system.nbody_to_si(total_mass,r)
    
    #Add Particles to Module
    for module in modules:
        module.particles.add_particles(experiment.particles)
    convert_nbody = None
    return modules, particles, convert_nbody

def run_experiment(experiment):
    from amuse.support.units import units, nbody_system
    time = 0 | experiment.timeUnit
    dt   = experiment.getTimeStep()
    tmax = experiment.stopTime
    

    modules, particles, convert_nbody = initialization(experiment)

    #Create channels Between Particles and Modules
    channels_to_module   = []
    channels_from_module = []
    for module in experiment.modules:
        channels_to_module.append(experiment.particles.new_channel_to(module.particles))
        channels_from_module.append(module.particles.new_channel_to(experiment.particles))

    while time <= tmax:
        #Evolve Modules
        for module in experiment.modules:
            module.evolve_model()
    	if 0 and len(modules)-1: #Currently disabled
    	        #Synchronize Particles Across Channels
    	        for channel in channels_from_module:
            	    channel.copy()
    	        for channel in channels_to_module:
    	            channel.copy()
        #Run Diagnostic Scripts
        for diagnostic in experiment.diagnostics:
            if diagnostic.shouldUpdate(time, particles):
                diagnostic.update(time,particles)
            
        #Run Logging Scripts
        for logger in experiment.loggers:
            logger.logData(particles)
            
        #Increment Time
        time += dt
        
    #Run Closing Diagnostic Scripts
    for diagnostic in experiment.diagnostics:
        if diagnostic.shouldUpdate(time,particles):
            diagnostic.update(time,particles)
    #Run Closing Logging Scripts
    for logger in experiment.loggers:
         logger.logData(experiment.particles)
    #Stop Modules
    for module in experiment.modules:
        module.stop()

if __name__ == "__main__":
    my_experiment = parse_flags()
    run_experiment(my_experiment)
    
    
