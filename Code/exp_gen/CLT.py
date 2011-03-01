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
def run_experiment(experiment):
    from amuse.support.units import units
    r    = 1 | units.pc
    time = 0 | experiment.timeUnit
    dt   = experiment.getTimeStep()
    tmax = experiment.stopTime
    
    #Initialize Particles
    #Create Conversion Object
    convert_nbody = nbody_system.nbody_to_si(1|units.MSun,r)
    #Create Module Objects
    #Add Particles to Module
    for module in experiment.modules:
        module.particles.add_particles(experiment.particles)
    #Create channels Between Particles and Modules
    channels_to_module   = []
    channels_from_module = []
    for module in experiment.modules:
        channels_to_module.append(experiment.particles.new_channel_to(module.particles))
        channels_from_module.append(module.particles.new_channel_to(experiment.particles))

    while t <= tmax:
        #Evolve Modules
        #Synchronize Particles Across Channels
        #Run Diagnostic Scripts
        #Run Logging Scripts
        #Increment Time
        t += dt
    #Run Closing Diagnostic Scripts
    #Run Closing Logging Scripts
    #Stop Modules

if __name__ == "__main__":
    my_experiment = parse_flags()
    
