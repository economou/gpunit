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

import amuse.support.io
from amuse.support.data.core import Particles
from amuse.support.units import units
from amuse.support.units.si import *
from amuse.support.units.units import *

from module import Module

defaultTimeStep = .1
defaultStartTime = 0
defaultStopTime = 100

XML_ENCODING = "UTF-8"

#Modified code to allow Use AMUSE units
defaultTimeUnit = units.yr #UnitType.yr

ModulePaths = {
    "hermite0" : "exp_management/Modules_XML/hermite0.xml",
    "ph4" : "exp_management/Modules_XML/ph4.xml",
}
'''File paths for Module XML file definitions'''

class Experiment:
    '''Experiment class holds all relevant experiment data
    for an AMUSE simulation'''

    def __init__(self, name = "") :
        #Constructor initializes the experiment to default values
        self.name = name
        self.stopIsEnabled = True
        self.modules = []

        self.particles = Particles(0)
        self.particlesPath = ""

        self.diagnostics = []
        self.diagnosticPaths = {}

        self.loggers = []
        self.loggerPaths = {}

        self.initialConditions = []
        self.initialConditionPaths = {}

        self.timeUnit  = defaultTimeUnit
        self.startTime = defaultStartTime | self.timeUnit
        self.stopTime  = defaultStopTime  | self.timeUnit
        self.timeStep  = defaultTimeStep  | self.timeUnit

    def copy(self):
        ret = experiment(self.name)

        ret.stopIsEnabled = self.stopIsEnabled
        ret.modules = self.modules[:]

        ret.particles = self.particles.copy()
        ret.particlesPath = self.particlesPath

        ret.diagnostics = self.diagnostics[:]
        ret.diagnosticPaths = self.diagnosticPaths.copy()

        ret.loggers = self.loggers[:]
        ret.loggerPaths = self.loggerPaths.copy()

        ret.initialConditions = self.initialConditions[:]
        ret.initialConditionPaths = self.initialConditionPaths.copy()

        ret.timeUnit  = self.timeUnit
        ret.startTime = self.startTime
        ret.stopTime  = self.stopTime
        ret.timeStep  = self.timeStep

    def toXML(self):
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

        for init in self.initialConditions:
            path = self.initialConditionPaths[init]

            initFile = open(path, "w")
            cPickle.dump(init, initFile)
            initFile.close()

            etree.SubElement(experiment, "initialCondition", attrib = {"file" : path})

        if len(self.particles) > 0:
            etree.SubElement(experiment, "particles", attrib = {"file" : self.particlesPath})
            amuse.support.io.write_set_to_file(self.particles, self.particlesPath, "hdf5")

        for diag in self.diagnostics:
            path = self.diagnosticPaths[diag]

            diagFile = open(path, "w")
            cPickle.dump(diag, diagFile)
            diagFile.close()

            etree.SubElement(experiment, "diagnostic", attrib = {"file" : path})

        for logger in self.loggers:
            path = self.loggerPaths[logger]

            loggerFile = open(path, "w")
            cPickle.dump(diag, loggerFile)
            loggerFile.close()

            etree.SubElement(experiment, "logger", attrib = {"file" : path})
        
        return xml.dom.minidom.parseString(etree.tostring(experiment, encoding = XML_ENCODING)).toprettyxml(encoding = XML_ENCODING)

    def writeXMLFile(self, filename):
        #Write th to the given file 
        outFile = open(fileName, 'w')
        outFile.write(self.toXML())

    @staticmethod
    def fromFile(filename):
        xml = ""
        expFile = open(filename, "r")
        for line in expFile:
            xml += line

        return Experiment.fromXML(xml)

    @staticmethod
    def fromXML(XMLString) :
        ret = Experiment()

        expElement = etree.fromstring(XMLString)
        
        # Extract Experiment's properties from XML attributes and sub-elements
        ret.name = expElement.get("name").strip()
        ret.stopIsEnabled = eval(expElement.get("stopEnabled").strip().title())
        
        timeElement = expElement.find("time")
        ret.timeUnit = eval(timeElement.get("units").strip())
        ret.startTime = float(timeElement.get("start").strip()) | ret.timeUnit
        ret.timeStep = float(timeElement.get("step").strip()) | ret.timeUnit
        ret.stopTime = float(timeElement.get("end").strip()) | ret.timeUnit

        for moduleElement in expElement.findall("module"):
            moduleName = moduleElement.get("name").strip()
            #look up file and parse it
            modFile = open(ModulePaths[moduleName], "r")
            xml = ""
            for line in modFile:
                xml += line
            modFile.close()
            module = Module.fromXML(xml)
            ret.modules.append(module)
        
        for initialConditionElement in expElement.findall("initialCondition"):
            path = initialConditionElement.get("file").strip()

            initCondFile = open(path, 'r')
            initCond = cPickle.load(initCondFile)
            initCondFile.close()

            ret.initialConditions.append(initCond)
            ret.initialConditionPaths[initCond] = path
        
        for loggerElement in expElement.findall("logger"):
            path = loggerElement.get("file").strip()

            loggerFile = open(path, 'r')
            logger = cPickle.load(loggerFile)
            loggerFile.close()

            ret.loggers.append(logger)
            ret.loggerPaths[logger] = path

        for diagnosticElement in expElement.findall("diagnostic"):
            path = diagnosticElement.get("file").strip()

            diagnosticFile = open(path, 'r')
            diag = cPickle.load(diagnosticFile)
            diagnosticFile.close()

            ret.diagnostics.append(diag)
            ret.diagnosticPaths[diag] = path

        particlesElement = expElement.find("particle")
        if particlesElement is not None:
            ret.particlesPath = particlesElement.get("file").strip()
            ret.particles = amuse.support.io.read_set_from_file(particlesPath, "hdf5")

        return ret

    def addDiagnostic(self, diag, filename = ""):
        self.diagnostics.append(diag)
        self.diagnosticPaths[diag] = filename

    def addLogger(self, logger, filename = ""):
        self.loggers.append(logger)
        self.loggerPaths[logger] = filename

    def addInitialCondition(self, init, filename = ""):
        self.initialConditions.append(init)
        self.initialConditionPaths[init] = filename

    def removeDiagnostic(self, diag):
        if diag in self.diagnostics:
            self.diagnostics.remove(diag)
            del self.diagnosticPaths[diag]

    def removeLogger(self, logger):
        if logger in self.loggers:
            self.loggers.remove(logger)
            del self.loggerPaths[logger]

    def removeInitialCondition(self, init):
        if init in self.initialCondition:
            self.initialConditions.remove(init)
            del self.initialConditionPaths[init]

    def __getstate__(self):
        return self.toXML()

    def __setstate__(self, state):
        exp = Experiment.fromXML(state)
        self.__dict__ = exp.__dict__.copy()
