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

from time import sleep
from time import time as gettime

from amuse.support.units import nbody_system
from amuse.support.units import units 
from amuse.support.data.particles import Particles

from exp_management.experiment import Experiment
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
            pass
        # Experiment needs the ability to have a number of particles for init
        # conditions set.
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

def initialization(experiment):
    '''
       Takes in an experiment object, parses the initialization.
       Take the initialization to initialize and return:
            modules:       Actual objects ready to  use for evolve_model
            particles:     AMUSE Particles class of all particles
            convert_nbody: Used for converting between nbody units and regular units
    '''
    r = 1 | units.parsec #Placeholder till we do this right.
    total_mass = 1.0 | units.MSun

    #Create Conversion Object
    convert_nbody = nbody_system.nbody_to_si(total_mass,r)

    particles = Particles()

    for pd in filter(lambda x: isinstance(x, ParticleDistribution), experiment.initialConditions):
        pd.convert_nbody = convert_nbody
        particles.add_particles(pd.getParticleList())

    #Total mass used for conversion object
    #total_mass = reduce(lambda x,y:x+y, particles.mass)

    # Build a set of arguments for the module constructors.
    args = [convert_nbody,]
    kwargs = {}

    #Get instances of actual AMUSE module classes from our wrappers.
    modules = [mod.instantiate(*args, **kwargs) for mod in experiment.modules]

    if experiment.scaleToStandard:
        particles.scale_to_standard(convert_nbody)

    #Add Particles to Module
    for module in modules:
        module.particles.add_particles(particles)

    return modules, particles, convert_nbody

def run_experiment(experiment):
    from amuse.support.units import units, nbody_system

    time = experiment.startTime
    dt   = experiment.timeStep
    tmax = experiment.stopTime

    modules, particles, convert_nbody = initialization(experiment)

    for module in modules:
        module.particles.copy_values_of_state_attributes_to(particles)

    for diagnostic in experiment.diagnostics:
        diagnostic.convert_nbody = convert_nbody
        diagnostic.preRunInitialize()

    # TODO: this is kinda a hack, need to add custom initialization code for
    # certain modules. In this case, PH4 needs its own internal timestep
    # parameter to be set explicitly (I think? This makes it not crash).
    from amuse.community.ph4.interface import ph4
    if isinstance(modules[0], ph4):
        modules[0].set_eta(experiment.timeStep.number)

    while time < tmax:
        #Evolve Modules
        for module in modules:
            module.evolve_model(time)

        for module in modules:
            module.particles.copy_values_of_state_attributes_to(particles)

        #Run Diagnostic Scripts
        for diagnostic in experiment.diagnostics:
            if diagnostic.shouldUpdate(time, modules):
                diagnostic.update(time,particles,modules)

        #Run Logging Scripts
        for logger in experiment.loggers:
            logger.logData(particles)

        #Increment Time
        time += dt

    #Run Closing Diagnostic Scripts
    for diagnostic in experiment.diagnostics:
        if diagnostic.shouldUpdate(time,modules):
            diagnostic.update(time,particles,modules)

    #Run Closing Logging Scripts
    for logger in experiment.loggers:
        logger.logData(experiment.particles)

    #Stop Modules
    for module in modules:
        module.stop()
    return time, dt, tmax, modules, experiment.loggers, experiment.diagnostics, particles

if __name__ == "__main__":
    my_experiment = parse_flags()
    run_experiment(my_experiment)
