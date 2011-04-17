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

import os

#Need to document these dependencies -- elementTree,minidom
import xml.etree.ElementTree as etree
import xml.dom.minidom

defaultTimeStep = 1
defaultStartTime = 0
defaultStopTime = 100

#Modified code to allow Use AMUSE units
defaultTimeUnit = units.yr #UnitType.yr

ModulePaths = {
    "hermite0" : "exp_management/ModulesXML"
}
'''File paths for Module XML file definitions'''

class Experiment :
    '''Experiment class holds all relevant experiment data
    for an AMUSE simulation'''

    def __init__(self, name) :
        #Constructor initializes the experiment to default values
        self.name = name
        self.stopIsEnabled = True
        self.modules = []
        self.particles = []
        self.particlesPath = ""
        self.diagnostics = []
        self.diagnosticsPaths = []
        self.loggers = []
        self.loggersPaths = []
        self.initialConditions = []
        self.initialConditionPaths = []
        self.timeUnit  = defaultTimeUnit
        self.startTime = defaultStartTime | self.timeUnit
        self.stopTime  = defaultStopTime  | self.timeUnit
        self.timeStep  = defaultTimeStep  | self.timeUnit

    def writeXMLFile(self,fileName) :
    
        # Create <experiment> XML element and set its attributes
        experiment = etree.Element("experiment", attrib = {"name" : self.name, "stopEnabled" : str(self.stopIsEnabled)})
        
        # Append sub-elements
        etree.SubElement(experiment, "time",
            attrib = {
                "units" : self.timeUnit._name_,
                "start" : str(self.startTime.number),
                "step"  : str(self.timeStep.getValue()),
                "end"   : str(self.stopTime.number)    
            }
        )
        
        for module in self.modules :
            etree.SubElement(experiment, "module", attrib = {"name" : module.name})

        for ic in self.initialConditionPaths :
            etree.SubElement(experiment, "initialCondition", attrib = {"file" : ic})    

        etree.SubElement(experiment, "particles", attrib = {"file" : self.particlesPath})

        for diag in self.diagnosticsPaths :
            etree.SubElement(experiment, "diagnostic", attrib = {"file" : diag})

        for logger in self.loggersPaths :
            etree.SubElement(experiment, "logger", attrib = {"file" : logger})
        
        # Prettify the XML
        uglyXml = xml.dom.minidom.parseString(etree.tostring(experiment, encoding = XML_ENCODING))
        
      #Write it to the given file 
        outFile = open(fileName, 'w')
        outFile.write(uglyXml.toprettyxml(encoding = XML_ENCODING))

#---------------------------------------------------
    def fromXML(self, XMLString) :
        pass #Just a place holder so code compiles
        #loads in the XML
        expElement = etree.fromstring(element)
        
        # Extract Experiment's properties from XML attributes and sub-elements
        self.name = expElement.get("name").strip()
        self.stopIsEnabled = eval(expElement.get("stopEnabled").strip().title())
        
        timeElement        = expElement.find("time")
        self.timeUnit      = timeElement.get("units").strip()
        self.startTime     = int(timeElement.get("start").strip()) | self.timeUnit
        self.timeStep      = int(timeElement.get("step").strip()) | self.timeUnit
        self.stopTime      = int(timeElement.get("end").strip()) | self.timeUnit

        for moduleElement in expElement.findall("module"):
            moduleName = moduleElement.get("name").strip()
            #look up file and parse it
            modFile = open(ModulePaths[moduleName], "r")
            xml = ""
            for line in modFile:
                xml += line
            modFile.close()
            module = Module.Module.fromXml(xml)
            self.modules.append(module)
        
        for initialConditionElement in expElement.findall("initialCondition"):
            initialConditionName = initialConditionElement.get("file").strip()
            #unpickle here
            self.initialConditions.append(#put model here)
        
        for loggerElement in expElement.findall("logger"):
            loggerPath = loggerElement.get("file").strip()
            #unpickle here
            self.loggers.append(#put loggers in here)

        for diagnosticElement in expElement.findall("diagnostic"):
            diagnosticPath = diagnosticElement.get("file").strip()
            #unpickle here
            self.diagnostics.append(#put diags in here)

        for particlesElement in expElement.findall("particle"):
            particlePath = particlesElement.get("file").strip()
            #unpickle here
            self.particles.append(#put particles in here)

        return
        
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


