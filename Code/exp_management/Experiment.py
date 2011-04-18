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


import os
import cPickle

#Need to document these dependencies -- elementTree,minidom
import xml.etree.ElementTree as etree
import xml.dom.minidom

from amuse.support.units import units
from amuse.support.units.si import *
from amuse.support.units.units import *

from Module import Module

defaultTimeStep = 1
defaultStartTime = 0
defaultStopTime = 100

XML_ENCODING = "UTF-8"

#Modified code to allow Use AMUSE units
defaultTimeUnit = units.yr #UnitType.yr

ModulePaths = {
    "hermite0" : "exp_management/Modules_XML/hermite0.xml"
}
'''File paths for Module XML file definitions'''

class Experiment :
    '''Experiment class holds all relevant experiment data
    for an AMUSE simulation'''

    def __init__(self, name = None) :
        #Constructor initializes the experiment to default values
        self.name = name
        self.stopIsEnabled = True
        self.modules = []
        self.particles = None
        self.particlesPath = ""
        self.diagnostics = []
        self.loggers = []
        self.initialConditions = []
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
                "units" : str(self.timeUnit),
                "start" : str(self.startTime.number),
                "step"  : str(self.timeStep.number),
                "end"   : str(self.stopTime.number)
            }
        )
        
        for module in self.modules :
            etree.SubElement(experiment, "module", attrib = {"name" : module.name})

        for ic in self.initialConditions :
            icFile = open(ic[1], "w")
            cPickle.dump(ic[0], icFile)
            icFile.close()

            etree.SubElement(experiment, "initialCondition", attrib = {"file" : ic[1]})

        etree.SubElement(experiment, "particles", attrib = {"file" : self.particlesPath})
        particlesFile = open(self.particlesPath, "w")
        cPickle.dump(self.particles, particlesFile)
        particlesFile.close()

        for diag in self.diagnostics :
            etree.SubElement(experiment, "diagnostic", attrib = {"file" : diag[1]})

        for logger in self.loggers :
            etree.SubElement(experiment, "logger", attrib = {"file" : logger[1]})
        
        uglyXml = xml.dom.minidom.parseString(etree.tostring(experiment, encoding = XML_ENCODING))
        
      #Write it to the given file 
        outFile = open(fileName, 'w')
        outFile.write(uglyXml.toprettyxml(encoding = XML_ENCODING))

#---------------------------------------------------
    def fromXML(self, XMLString) :
        expElement = etree.fromstring(XMLString)
        
        # Extract Experiment's properties from XML attributes and sub-elements
        self.name = expElement.get("name").strip()
        self.stopIsEnabled = eval(expElement.get("stopEnabled").strip().title())
        
        timeElement        = expElement.find("time")
        self.timeUnit      = eval(timeElement.get("units").strip())
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
            module = Module.fromXML(xml)
            self.modules.append(module)
        
        for initialConditionElement in expElement.findall("initialCondition"):
            path = initialConditionElement.get("file").strip()

            initCondFile = open(path, 'r')
            initCond = cPickle.load(initCondFile)
            initCondFile.close()

            self.initialConditions.append((initCond, path))
        
        for loggerElement in expElement.findall("logger"):
            path = loggerElement.get("file").strip()

            loggerFile = open(path, 'r')
            logger = cPickle.load(loggerFile)
            loggerFile.close()

            self.loggers.append((logger, path))

        for diagnosticElement in expElement.findall("diagnostic"):
            path = diagnosticElement.get("file").strip()

            diagnosticFile = open(path, 'r')
            diag = cPickle.load(diagnosticFile)
            diagnosticFile.close()

            self.diagnostics.append((diag, path))

        particlesElement = expElement.find("particle")
        if particlesElement is not None:
            self.particlesPath = particlesElement.get("file").strip()

            particlesFile = open(self.particlesPath, 'r')
            self.particles = cPickle.load(particlesFile)
            particlesFile.close()

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


