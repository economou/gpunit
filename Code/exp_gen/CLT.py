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

def run_experiment(experiment):
    from amuse.support.units import units, nbody_system
    r    = 1 | units.parsec
    time = 0 | experiment.timeUnit
    dt   = experiment.getTimeStep()
    tmax = experiment.stopTime
    
    modules = [mod.result for mod in experiment.modules()]
    particles = experiment.particles


    #Initialize Particles
    #Create Conversion Object
    convert_nbody = nbody_system.nbody_to_si(1|units.MSun,r)
    #Create Module Objects
    #Add Particles to Module
    for module in modules:
        module.particles.add_particles(experiment.particles)

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
            if diagnostic.shouldUpdate(None):
                diagnostic.update(particles)
            
        #Run Logging Scripts
        for logger in experiment.loggers:
            logger.logData(experiment.particles)
            
        #Increment Time
        time += dt
    #Run Closing Diagnostic Scripts
    for diagnostic in experiment.diagnostics:
        if diagnostic.shouldUpdate(None):
            diagnostic.update(experiment.particles)
    #Run Closing Logging Scripts
    for logger in experiment.loggers:
         logger.logData(experiment.particles)
    #Stop Modules
    for module in experiment.modules:
        module.stop()

if __name__ == "__main__":
    my_experiment = parse_flags()
    run_experiment(my_experiment)
    
    
