#!/usr/bin/env python

"""Defines classes for the representation of and interaction with AMUSE modules,
including several ancillary types utilized by the module implementation.

Author: Jason Economou, Gabriel Schwartz
Last Modified: 5/31/11"""

from amuse.support.exceptions import AmuseException
from amuse.support.units.core import IncompatibleUnitsException

from PyQt4.QtGui import QListWidgetItem

try:
    from lxml import etree
    usingLXML = True
except:
    import xml.etree.ElementTree as etree
    usingLXML = False

import re
import os
import sys

# OrderedDict is new to 2.7
try:
	from collections import OrderedDict
except ImportError:
	class OrderedDict(dict):
		pass

from parameters import Parameter, BoolParameter
from exp_design.settings import SettingsDialog

XML_ENCODING = "UTF-8"

ModuleDir = os.path.abspath("exp_management/Modules_XML/")
ModulePaths = {
    "hermite0" : os.path.join(ModuleDir,"hermite0.xml"),
    "ph4" : os.path.join(ModuleDir,"ph4.xml"),
    "phiGRAPE" : os.path.join(ModuleDir,"phigrape.xml"),
    "octgrav" : os.path.join(ModuleDir,"octgrav.xml"),
    "BHTree" : os.path.join(ModuleDir,"bhtree.xml"),
}
"""File paths for Module definition XML files distributed with GPUnit."""

AstrophysicalDomains = (
    "Stellar Dynamics",
    "Stellar Evolution",
    "Hydrodynamics",
    "Radiative Transfer"
)
"""Types of codes supported by AMUSE."""

StoppingConditions = {
#    "None"              : 0,
    "Collision"         : 1,
    "Pair"              : 2,
    "Escaper"           : 4,
    "Timeout"           : 8,
    "Number Of Steps"   : 16,
    "Out Of Box"        : 32
}
"""Stopping conditions for an AMUSE module.  This dictionary simulates a flags
enumeration.  For modules with multiple stopping conditions, the values of this
enumeration may be added together.

StoppingConditions is a set of bit flags enumerating the conditions under which
a module may return from execution before completing its assigned
calculations."""

class Module(QListWidgetItem):
    """A particular AMUSE module, providing an interface between GPUnit and
    the AMUSE code. The members of the Module class are used by GPUnit to
    properly locate and initialize an AMUSE module, as well as display a
    module's details and configuration to the user in the graphical
    interface."""

    # Constructor
    def __init__(self,
            name = "Module",
            description = "Description...",
            domain = "StellarEvolution",
            className = "ClassName",
            codeLocation = "amuse/path/to/code/location",
            isParallel = False,
            stoppingConditions = [],
            stoppingConditionsEnabled = [],
            parameters = []):

        """Initializes a new Module with the given instance data.
          @param name: The full name of the module.
          @param description: A description of the module's purpose (in other
            words, the calculations performed by the module).
          @param domain: The astrophysical domain into which the module has
            been sorted.
          @param className: The name of the AMUSE class containing the module code.
          @param codeLocation: The location of the AMUSE module code.
          @param isParallel: Whether the module's calculations can be
            parallelized across multiple workers by MPI.
          @param stoppingConditions: The condition(s) under which the module
            may stop executing prematurely.
          @param parameters: The module parameters.  These module-specific
            values may be modified prior to running the experiment in order to
            fine-tune the module's behavior."""

        self.name = name
        self.description = description
        self.domain = domain
        self.codeLocation = codeLocation
        self.isParallel = isParallel
        self.stoppingConditions = stoppingConditions
        self.stoppingConditionsEnabled = stoppingConditionsEnabled
        self.parameters = parameters
        self.className  = className
        self.interfaceName = None

        # Set up the module's name so that it can be displayed in GUI list boxes
        QListWidgetItem.__init__(self)
        self.setText(self.name)

    # Methods
    def toXML(self):
        """Dumps the Module to an XML string.

        Output:
          A string containing an XML representation of the Module."""
        
        module = etree.Element("Module", attrib={"name" : self.name})

        description = etree.SubElement(module, "description")
        description.text = self.description

        domain = etree.SubElement(module, "domain")
        domain.text = self.domain

        className = etree.SubElement(module, "className")
        className.text = self.className

        codeLocation = etree.SubElement(module, "codeLocation")
        codeLocation.text = self.codeLocation

        # Interface Name might not be known for all modules so this is
        # optional.
        if self.interfaceName is not None:
            interfaceName = etree.SubElement(module, "interfaceName")
            interfaceName.text = self.interfaceName

        isParallel = etree.SubElement(module, "isParallel")
        isParallel.text = str(self.isParallel)

        stoppingConditions = etree.SubElement(module, "stoppingConditions")
        stopcond = 0
        for cond in self.stoppingConditions:
            stopcond = stopcond | StoppingConditions[cond]
        stoppingConditions.text = str(stopcond)

        parameters = etree.SubElement(module, "parameters")
        for parameter in self.parameters:
            parameter.appendToXMLElement(parameters)

        if usingLXML:
            return etree.tostring(module, encoding = XML_ENCODING, pretty_print = True)
        else:
            return etree.tostring(module, encoding = XML_ENCODING)

    def toXMLPatch(self):
        module = etree.Element("ModulePatch", attrib={"name" : self.name})
        
        stoppingConditions = etree.SubElement(module, "stoppingConditionsEnabled")
        stopcond = 0
        for cond in self.stoppingConditionsEnabled:
            stopcond = stopcond | StoppingConditions[cond]
        stoppingConditions.text = str(stopcond)
        
        parameters = etree.SubElement(module, "parameters")
        for parameter in self.parameters:
            parameter.appendValueToXMLElement(parameters)
        
        if usingLXML:
            return etree.tostring(module, encoding = XML_ENCODING, pretty_print = True)
        else:
            return etree.tostring(module, encoding = XML_ENCODING)

    @staticmethod
    def fromFile(filename):
        xml = ""
        modFile = open(filename, "r")
        for line in modFile:
            xml += line
        if "ModulePatch" in xml:
            return Module.fromXMLPatch(xml)
        else:
            return Module.fromXML(xml)

    @staticmethod
    def fromXML(text):
        """Recreates a Module from its XML specification.

        Parameters:
          text -- A string containing an XML representation of a Module.

        Output:
          A Module whose properties are specified by the given XML text."""

        module = etree.fromstring(text)
        name = module.attrib["name"]

        # List of required child elements that consist solely of text.
        textChildren = (
                "description",
                "domain",
                "codeLocation",
                "isParallel",
                "stoppingConditions",
                "className",
                )

        textValues = {}

        # Pull out the text from all required text-only tags.
        for childTag in textChildren:
            element = module.find(childTag)

            if element is None:
                print "Missing required tag:", childTag + "."
                exit(1)

            textValues[childTag] = str(element.text)

        #description         = textValues["description"]
        # Eliminate extra whitespace
        description         = re.sub(r'\s+',r' ',textValues["description"].strip())
        domain              = textValues["domain"]
        className           = textValues["className"]
        codeLocation        = textValues["codeLocation"]
        stopcond            = int(textValues["stoppingConditions"])
        isParallel          = eval(textValues["isParallel"].title())

        # Interface Name might not be known for all modules so this is
        # optional.
        interfaceElement = module.find("interfaceName")

        interfaceName = None
        if interfaceElement is not None:
            interfaceName = interfaceElement.text

        stoppingConditions = []
        for cond, code in StoppingConditions.items():
            if stopcond & code:
                stoppingConditions.append(cond)

        parameters = []
        paramsElement = module.find("parameters")

        if paramsElement is not None:
            for param in paramsElement.findall("parameter"):
                parameters.append(Parameter.paramFromElement(param))

        module = Module(
                name,
                description,
                domain,
                className,
                codeLocation,
                isParallel,
                stoppingConditions,
                [],
                parameters)

        module.interfaceName = interfaceName

        return module
    
    @staticmethod
    def fromXMLPatch(text):
        module_elem = etree.fromstring(text)
        name = module_elem.attrib["name"]
        
        if name in ModulePaths:
            module = Module.fromFile(ModulePaths[name])
        else:
            module = Module()
        
        stoppingConditionsElement = module_elem.find("stoppingConditionsEnabled")
        stopcond = int(stoppingConditionsElement.text or 0) #TODO consider exception handling
        for cond in StoppingConditions:
            if cond in module.stoppingConditions and StoppingConditions[cond] & stopcond:
                module.stoppingConditionsEnabled.append(cond)
        
        paramsElement = module_elem.find("parameters")
        if paramsElement is not None:
            for param in paramsElement.findall("parameter"):
                if "value" in param.attrib:
                    module_param = module.parameterByName(param.attrib["name"])
                    if module_param is not None:
                        module_param.value = param.attrib["value"]
        
        return module
        

    def instantiate(self, convert_nbody):
        """Returns an instance of the amuse module."""

        filename = re.search("(?<=/)[\da-zA-Z]*\.py$", self.codeLocation).group(0).rstrip(".py")
        if self.codeLocation[:5] == 'amuse':
            path = ".".join(self.codeLocation.split("/"))[:-3]
            exec("from " + path + " import " + self.className)

            if self.interfaceName is not None:
                exec("from "+ path + " import " + self.interfaceName)
        else:
            sys.path.append(self.codeLocation.rstrip(filename))
            exec("from " + filename + " import " + self.className)

            if self.interfaceName is not None:
                exec("from "+ filename + " import " + self.interfaceName)

        args = [convert_nbody,]

        paramNames = [param.name for param in self.parameters]
        paramValues = [eval(str(param.value)) for param in self.parameters]
        paramUnits = [param.unit for param in self.parameters]

        kwargs = dict(zip(paramNames, paramValues))
        
        exec("r_val = %s(*args, **kwargs)" % str(self.className))
        
        r_val.initialize_code()
        r_val.parameters.set_defaults()
        for name,value,unit in zip(paramNames,paramValues,paramUnits):
            try:
                r_val.parameters.get_parameter(name).set_value(value | unit)
            except IncompatibleUnitsException:
                print "warning: invalid units for",self.name,"module's",name,"parameter--ignoring parameter"
            except AmuseException:
                print "warning: unrecognized parameter",name,"for",self.name,"module--ignoring parameter"
        r_val.commit_parameters()
        
        for cond in self.stoppingConditionsEnabled:
            text = cond.lower().replace(' ','_')
            exec("r_val.stopping_conditions.%s_detection.enable()" % text)
        
        return r_val

    def parameterByName(self, name):
        for param in self.parameters:
            if param.name == name:
                return param

        return None

    def showSettingsDialog(self):
        if len(self.parameters) < 1:
            return

        inputs = OrderedDict()
        defaults = OrderedDict()

        for param in self.parameters:
            name, default, value = param.getSettingsEntry()
            inputs[name] = value
            defaults[name] = default
        
        # Pseudo-parameters for stopping conditions
        scFormat = "Enable %s detection"
        for cond in self.stoppingConditions:
            param = BoolParameter(scFormat % cond,False,cond in self.stoppingConditionsEnabled)
            name, default, value = param.getSettingsEntry()
            inputs[name] = value
            defaults[name] = default

        settings = SettingsDialog(inputs, defaults)
        results = settings.getValues()

        # Disable all stopping conditions; will re-enable those that were checked
        self.stoppingConditionsEnabled = []

        if len(results) > 0:
            for name, value in results.items():
                param = self.parameterByName(name)
                if param is not None:
                    param.value = value
                elif value: # must be stopping condition
                    namepos = scFormat.find('%s')
                    namelen = len(name) - (len(scFormat) - 2)
                    self.stoppingConditionsEnabled.append(name[namepos:namepos+namelen])
