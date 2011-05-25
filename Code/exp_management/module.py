#!/usr/bin/env python

'''Defines classes for the representation of and interaction with AMUSE modules,
including several ancillary types utilized by the module implementation.

Author:
  Jason Economou

Date:
  01 March 2011

State:
  Preliminary'''

from PyQt4.QtGui import QListWidgetItem

import xml.etree.ElementTree as etree
import xml.dom.minidom
import re
import os
import sys

XML_ENCODING = "UTF-8"

ModulePaths = {
    "Gravity (hermite0)" : "exp_management/Modules_XML/hermite0.xml",
    "Gravity (ph4)" : "exp_management/Modules_XML/ph4.xml",
    "Gravity (phiGRAPE)" : "exp_management/Modules_XML/phigrape.xml",
}
'''File paths for Module XML file definitions'''

AstrophysicalDomains = (
    "Stellar Dynamics",
    "Stellar Evolution",
    "Hydrodynamics",
    "Radiative Transfer"
)
"""Types of codes supported by AMUSE."""

StoppingConditions = {
    "None"              : 0,
    "Collision"         : 1,
    "Pair"              : 2,
    "Escaper"           : 4,
    "Timeout"           : 8,
    "Number Of Steps"   : 16,
    "Out Of Box"        : 32
}
'''Stopping conditions for an AMUSE module.  This dictionary simulates a flags
enumeration.  For modules with multiple stopping conditions, the values of this
enumeration may be added together.

StoppingConditions is a set of bit flags enumerating the conditions under which
a module may return from execution before completing its assigned
calculations.'''

class Module(QListWidgetItem):
    '''A particular AMUSE module, providing an interface between GPUnit and
    the AMUSE code. The members of the Module class are used by GPUnit to
    properly locate and initialize an AMUSE module, as well as display a
    module's details and configuration to the user in the graphical
    interface.'''

    # Constructor
    def __init__(self,
            name = "Module",
            description = "Description...",
            domain = "StellarEvolution",
            className = "ClassName",
            codeLocation = "amuse/path/to/code/location",
            isParallel = False,
            stoppingConditions = [],
            parameters = [],
            classname = None):

        '''Initializes a new Module with the given instance data.
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
            fine-tune the module's behavior.
          @param classname: The name of the class inside the AMUSE module one will be using.'''

        self.name = name
        self.description = description
        self.domain = domain
        self.codeLocation = codeLocation
        self.isParallel = isParallel
        self.stoppingConditions = stoppingConditions
        self.parameters = parameters
        self.className  = className

        # Set up the module's name so that it can be displayed in GUI list boxes
        QListWidgetItem.__init__(self)
        self.setText(self.name)

    # Methods
    def toXML(self):
        '''Dumps the Module to an XML element.

        The element is formatted as follows:
        <Module name="Example">
          <description>
            Calculates the temporal discombobulation of the flux capacitor over time.
          </description>
          <domain>
            Stellar Dynamics
          </domain>
          <className>
            Example
          </className>
          <codeLocation>
            src/amuse/community/example/example.py
          </codeLocation>
          <isParallel>
            false
          </isParallel>
          <stoppingConditions>
            0
          </stoppingConditions>
          <Parameter ...>
            ...
          </Parameter>
          ...
        </Module>

        Output:
          A string containing an XML representation of the Module.'''

        # Create <Module> XML element and set its attributes
        module = etree.Element("Module", attrib = {"name" : self.name})

        # Append simple sub-elements
        description = etree.SubElement(module, "description")
        description.text = self.description

        domain = etree.SubElement(module, "domain")
        domain.text = self.domain

        className = etree.SubElement(module, "className")
        className.text = self.className

        codeLocation = etree.SubElement(module, "codeLocation")
        codeLocation.text = self.codeLocation

        isParallel = etree.SubElement(module, "isParallel")
        isParallel.text = str(self.isParallel)  # Convert boolean to string for serialization

        stoppingConditions = etree.SubElement(module, "stoppingConditions")

        stopcond = 0
        for cond in self.stoppingConditions:
            stopcond = stopcond | StoppingConditions[cond]

        stoppingConditions.text = str(stopcond)  # Convert integer to string for serialization

        # Iterate through parameters and append them as sub-elements
        for parameter in self.parameters:
            module.append(etree.fromstring(parameter.toXML()))

        # Prettify the XML
        uglyXml = xml.dom.minidom.parseString(etree.tostring(module, encoding = XML_ENCODING))

        return uglyXml.toprettyxml(encoding = XML_ENCODING)

    @staticmethod
    def fromFile(filename):
        xml = ""
        modFile = open(filename, "r")
        for line in modFile:
            xml += line

        return Module.fromXML(xml)

    @staticmethod
    def fromXML(element):
        '''Recreates a Module from its XML specification.

        Parameters:
          element -- A string containing an XML representation of a Module.

        Output:
          A Module whose properties are specified by the given XML element.'''

        # Parse Module from XML
        moduleElement = etree.fromstring(element)

        # Extract Module's properties from XML attributes and sub-elements
        name = moduleElement.get("name")

        description        = moduleElement.find("description").text.strip()
        domain             = moduleElement.find("domain").text.strip()
        className          = moduleElement.find("className").text.strip()
        codeLocation       = moduleElement.find("codeLocation").text.strip()
        isParallel         = eval(moduleElement.find("isParallel").text.strip().title())  # Evaluate string as boolean
        stopcond           = int(moduleElement.find("stoppingConditions").text.strip())  # Parse integer from string.

        stoppingConditions = []
        for cond, code in StoppingConditions.items():
            if stopcond & code:
                stoppingConditions.append(cond)

        # Create the Module
        module = Module(name, description, domain, className, codeLocation, isParallel, stoppingConditions, [])

        # Iterate through Parameter elements and add Parameters to the Module
        for parameterElement in moduleElement.findall("Parameter"):
            parameter = Parameter.fromXML(etree.tostring(parameterElement, encoding = XML_ENCODING))
            module.addParameter(parameter)

        return module

    def addParameter(self, p):
        '''Adds the given parameter to this module.

        Parameters:
          p -- A module parameter to add to the module.'''

        self.parameters.append(p)

    def removeParameter(self, p):
        '''Removes the given parameter from this module, if the parameter exists.

        Parameters:
          p -- A module parameter to remove from the module.

        Output:
          Whether the given parameter was removed. Returns false if the parameter was not found in this module's parameter list.'''

        try:
            self.parameters.remove(p)
            return True
        except ValueError:
            return False

    def instantiate(self, *args, **kwargs):
        """Returns an instance of the amuse module."""

        filename = re.search("(?<=/)[\da-zA-Z]*\.py$", self.codeLocation).group(0)
        if self.codeLocation[:5] == 'amuse':
            path = ".".join(self.codeLocation.split("/"))[:-3]
            exec("from "+path+" import "+self.className)
        else:
            sys.path.append(self.codeLocation.rstrip(filename))
            exec("from " + filename.rstrip(".py") + " import " + self.className)

        exec("r_val = %s(*args, **kwargs)" % str(self.className))

        return r_val

class Parameter:
    '''A parameter to an AMUSE module.

    Modules have parameters that may be modified by the user via the
    graphical interface. These parameters are typically specific to the
    module's domain or even to the individual module. The Parameter class is
    a generic class whose type parameter specifies the type of the
    parameter's value (e.g. integer or floating-point). A parameter may be a
    physical quantity, flag, or other value.'''

    # Constructor
    def __init__(self, name, description, defaultValue, units):
        '''Initializes a new Parameter with the given instance data.

          @param name: The brief, descriptive name of the parameter.
          @param description: A description of the parameter's meaning and
          effects.
          @param defaultValue: The parameter's default value.
          @param units: The physical unit(s) associated with the parameter's
          value.'''

        self.name = name
        self.description = description
        self.defaultValue = defaultValue
        self.units = units

    # Methods
    def toXML(self):
        '''Dumps the Parameter to an XML element.

        The element is formatted as follows:
        <Parameter name="Example">
          <description>
            The current magnitude of the flux capacitance.
          </description>
          <defaultValue>
            0.88
          </defaultValue>
          <Units ...>
            ...
          </Units>
        </Parameter>

        Output:
          A string containing an XML representation of the Parameter.'''

        # Create <Parameter> XML element and set its attributes
        parameter = etree.Element("Parameter", attrib = {"name" : self.name})

        # Append sub-elements
        description = etree.SubElement(parameter, "description")
        description.text = self.description

        defaultValue = etree.SubElement(parameter, "defaultValue")
        defaultValue.text = str(self.defaultValue)  # Convert numbers to strings for serialization

        parameter.append(etree.fromstring(self.units.toXML()))

        return etree.tostring(parameter, encoding = XML_ENCODING)

    @staticmethod
    def fromXML(element):
        '''Recreates a Parameter from its XML specification.

        Parameters:
          element -- A string containing an XML representation of a Parameter.

        Output:
          A Parameter whose property values are specified by the given XML element.'''

        # Parse Parameter from XML
        parameterElement = etree.fromstring(element)

        # Extract Parameter's properties from XML attributes and sub-elements
        name = parameterElement.get("name")

        description  = parameterElement.find("description").text.strip()
        defaultValue = eval(parameterElement.find("defaultValue").text.title().strip())  # Evaluate strings as numbers

        # Read Units sub-element into a CompoundUnit instance
        unitsElement = parameterElement.find("Units")
        units        = CompoundUnit.fromXML(etree.tostring(unitsElement, encoding = XML_ENCODING))

        # Create the Parameter
        parameter = Parameter(name, description, defaultValue, units)

        return parameter

class CompoundUnit:
    '''A compound physical unit.

    When performing physical calculations, units of measure may combined in
    any number of ways. The CompoundUnit class provides the mechanism by
    which units may be presented to the user, regardless of whether they are
    simple or compound.'''

    # Constructor
    def __init__(self, description, symbolicDescription, units):
        '''Initializes a new CompoundUnit with the given instance data.

        Parameters:
          description -- A non-abbreviated textual description of the combined physical unit.
          symbolicDescription -- A shorthand textual description of the combined physical unit, using unit abbreviations.
          units -- The list of simple units whose combination is represented by this compound unit.'''

        self.description = description
        self.symbolicDescription = symbolicDescription
        self.units = units

    # Methods
    def toXML(self):
        '''Dumps the CompoundUnit to an XML element.

        The element is formatted as follows:
        <Units>
          <description>
            gigawatts per second
          </description>
          <symbolicDescription>
            GW/s
          </symbolicDescription>
          <Unit ...>
            ...
          </Unit>
          ...
        </Units>

        Output:
          A string containing an XML representation of the CompoundUnit.'''

        # Create <Units> XML element
        units = etree.Element("Units")

        # Append simple sub-elements
        description = etree.SubElement(units, "description")
        description.text = self.description

        symbolicDescription = etree.SubElement(units, "symbolicDescription")
        symbolicDescription.text = self.symbolicDescription

        # Iterate through simple units and append them as sub-elements
        for unit in self.units:
            units.append(etree.fromstring(unit.toXML()))

        return etree.tostring(units, encoding = XML_ENCODING)

    @staticmethod
    def fromXML(element):
        '''Recreates a CompoundUnit from its XML specification.

        Parameters:
          element -- A string containing an XML representation of a CompoundUnit.

        Output:
          A CompoundUnit whose property values are specified by the given XML element.'''

        # Parse CompoundUnit from XML
        unitsElement = etree.fromstring(element)

        # Extract CompoundUnit's properties from XML sub-elements
        description         = unitsElement.find("description").text.strip()
        symbolicDescription = unitsElement.find("symbolicDescription").text.strip()

        # Create the CompoundUnit
        units = CompoundUnit(description, symbolicDescription, [])

        # Iterate through simple Unit elements and add simple Units to the CompoundUnit
        for unitElement in unitsElement.findall("Unit"):
            unit = Unit.fromXML(etree.tostring(unitElement, encoding = XML_ENCODING))
            units.addUnit(unit)

        return units

    def addUnit(self, u):
        '''Adds the given unit to this compound unit's list of simple units.

        Parameters:
          u -- A unit to be included in this compound unit.'''

        self.units.append(u)

    def removeUnit(self, u):
        '''Removes the given simple unit from this compound unit, if the simple unit exists.

        Parameters:
          u -- A unit to remove from this compound unit.

        Output:
          Whether the given unit was removed. Returns false if the unit was not found in this instance's unit list.'''

        try:
            self.units.remove(u)
            return True
        except ValueError:
            return False

class Unit:
    '''A simple physical unit.

    With AMUSE, physical quantities may be expressed using, and converted
    between, a number of different standard units. The Unit class, in
    conjunction with the CompoundUnit class, allows GPUnit to present these
    units to the user for the purposes of description and selection.'''

    # Constructor
    def __init__(self, utype, prefix, exponent):
        '''Initializes a new Unit with the given instance data.

        Parameters:
          utype -- The base type of astrophysical unit being represented.
          prefix -- The SI prefix that modifies the base unit's order of magnitude.
          exponent -- The exponent to be applied to the unit. For example, a typical unit of volume (such as cubic meters) would have an exponent of 3.'''

        self.utype = utype
        self.prefix = prefix
        self.exponent = exponent

    # Methods
    def toXML(self):
        '''Dumps the Unit to an XML element.

        The element is formatted as follows:
        <Unit type="Watt" prefix="G" exponent="1" />

        Output:
          A string containing an XML representation of the Unit.'''

        # Create <Unit> XML element and set its attributes
        attrDict = {}
        if self.utype is not None:
            attrDict["type"] = self.utype
        if self.prefix is not None:
            attrDict["prefix"] = self.prefix
        if self.exponent is not None:
            attrDict["exponent"] = str(self.exponent)  # Convert integer to string for serialization

        unit = etree.Element("Unit", attrib = attrDict)

        return etree.tostring(unit, encoding = XML_ENCODING)

    @staticmethod
    def fromXML(element):
        '''Recreates a Unit from its XML specification.

        Parameters:
          element -- A string containing an XML representation of a Unit.

        Output:
          A Unit whose property values are specified by the given XML element.'''

        # Parse Unit from XML
        unitElement = etree.fromstring(element)

        # Extract Unit's properties from XML attributes
        utype    = unitElement.get("type")
        prefix   = unitElement.get("prefix")
        exponent = eval(unitElement.get("exponent"))  # Evaluate string as integer

        # Create the Parameter
        unit = Unit(utype, prefix, exponent)

        return unit
