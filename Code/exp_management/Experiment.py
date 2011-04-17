#!/usr/bin/python
#
# Experiment.py
#    The experiment class holds all relevant experiment data for
#    an AMUSE simulation.
#
# Andrew Sherman
# 2/11
#
# Team GPUnit - Senior Design 2011
#
#

from amuse.support.units import units

#Need to document this dependency -- minidom
from xml.dom import minidom

defaultTimeStep = 1
defaultStartTime = 0
defaultStopTime = 100

#Modified code to allow Use AMUSE units
defaultTimeUnit = units.yr #UnitType.yr

class Experiment :
    '''Experiment class holds all relevant experiment data
    for an AMUSE simulation'''

    def __init__(self, name) :
        #Constructor initializes the experiment to default values
        self.name = name
        self.stopIsEnabled = True
        self.modules = []
        self.particles = []
        self.diagnostics = []
        self.loggers = []
        self.timeUnit  = defaultTimeUnit
        self.startTime = defaultStartTime | self.timeUnit
        self.stopTime  = defaultStopTime  | self.timeUnit
        self.timeStep  = defaultTimeStep  | self.timeUnit

    def writeXMLFile(self,fileName) :
      #writes out the XML
        tabstop = '  ' #2 spaces for indentations aiding readability
        depth = 0
        XMLString = ""
      #Experiment tag
        XMLString += '<experiment name="'+self.name+'" stopEnabled="'+self.stopIsEnabled+'">\n'
        depth += 1
      #Time tag
        XMLString += tabstop*depth
        XMLString += '<time units="'+self.timeUnit._name_+'" start="'+self.startTime.number+'" step="'+self.timeStep.getValue()+'" end="'+self.stopTime+'"/>\n'
      #Module tags
        for module in self.modules :
            XMLString += tabstop*depth
            XMLString += module.toXml()
            XMLString += '\n'
            depth += 1
            for param in module.getParameters() :
                XMLString += tabstop*depth
                XMLString += param.toXml()
                XMLString += '\n'
            depth -= 1
      #Particle tags
        for particle in self.particles :
            XMLString += tabstop*depth
            XMLString += particle.toXml()
            XMLString += '\n'
      #Diagnostic tags
        for diag in self.diagnostics :
            XMLString += tabstop*depth
            XMLString += diag.toXml()
            XMLString += '\n'
      #Logger tags
        for logger in self.loggers :
            XMLString += tabstop*depth
            XMLString += logger.toXml()
            XMLString += '\n'
        XMLString += '</experiment>'
      #Write it to the given file 
        outFile = open(fileName, 'w')
        outFile.write(XMLString)

#---------------------------------------------------
    def loadXMLFile(self, fileName) :
        pass #Just a place holder so code compiles
        #loads in the XML
        #not sure what to do here yet
        #are we going to use minidom or something?
#---------------------------------------------------
        

    def getCurrentState(self) :
        #returns the list of particles to read their states
        return self.particles

#---------------------------------------------------
#Maybe this evolve method isn't needed?
#    def evolveState() :
        #Evolve the simulation
#---------------------------------------------------

    def setName(self, name) :
        #Sets the name of the experiment to the given value
        self.name = name

    def getName(self) :
        #Returns the name of the experiment
        return self.name

    def setTimeStep(self,timeStep) :
        #Sets the timestep to the given value
        self.timeStep = timeStep|self.timeUnit

    def getTimeStep(self) :
        #Returns the experiment's timeStep
        return self.timeStep

    def disableStopConditions(self) :
        #Disables the stopping conditions
        self.stopIsEnabled = False

    def enableStopConditions(self) :
        #Enables the stopping conditions
        self.stopIsEnabled = True

    def addModule(self, module) :
        #Adds the given module to the module list
        self.modules.append(module)

    def removeModule(self, module) :
        #Removes the given module from the module list
        self.modules.remove(module)

    def addModules(self, modules) :
        #Adds the given modules to the module list
        self.modules.extend(modules)

    def addParticle(self, particle) :
        #Adds the given particle to the particle list
        self.particles.append(particle)

    def removeParticle(self, particle) :
        #Removes the given particle from the particle list
        self.particles.remove(particle)

    def addParticles(self, particles) :
        #Adds the given particles to the particle list
        self.particles.extend(particles)

    def addDiagnostic(self, diagnostic) :
        #Adds the given diagnostic to the diagnostic list
        self.diagnostics.append(diagnostic)

    def removeDiagnostic(self, diagnostic) :
        #Removes the given diagnostic from the diagnostic list
        self.diagnostics.remove(diagnostic)

    def addDiagnostics(self, diagnostics) :
        #Adds the given diagnostics to the diagnostic list
        self.diagnostics.extend(diagnostics)

    def addLogger(self, logger) :
        #Adds the given logger to the logger list
        self.loggers.append(logger)

    def removeLogger(self, logger) :
        #Removes the given logger from the logger list
        self.loggers.remove(logger)

    def addLoggers(self, loggers) :
        #Adds the given loggers to the logger list
        self.loggers.extend(loggers)


