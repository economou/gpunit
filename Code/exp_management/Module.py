#!/usr/bin/env python

'''Defines classes for the representation of and interaction with AMUSE modules,
including several ancillary types utilized by the module implementation.

Author:
  Jason Economou

Date:
  01 March 2011

State:
  Preliminary'''

# TODO: Enforce type safety?
# TODO: Implement enumerations?  If so, to what degree?

import xml.etree.ElementTree as etree
import xml.dom.minidom

class Module:
	'''A particular AMUSE module, providing an interface between GPUnit and
	the AMUSE code. The members of the Module class are used by GPUnit to
	properly locate and initialize an AMUSE module, as well as display a
	module's details and configuration to the user in the graphical
	interface.'''
	
	# Constructor
	def __init__(self, name, description, domain, codeName, codeLocation, isParallel, stoppingConditions, parameters):
		'''Initializes a new Module with the given instance data.
		
		Parameters:
		  name -- The full name of the module.
		  description -- A description of the module's purpose (in other words, the calculations performed by the module).
		  domain -- The astrophysical domain into which the module has been sorted.
		  codeName -- The name of the AMUSE class containing the module code.
		  codeLocation -- The location of the AMUSE module code.
		  isParallel -- Whether the module's calculations can be parallelized across multiple workers by MPI.
		  stoppingConditions -- The condition(s) under which the module may stop executing prematurely.
		  parameters -- The module parameters.  These module-specific values may be modified prior to running the experiment in order to fine-tune the module's behavior.'''
		
		self.name = name
		self.description = description
		self.domain = domain
		self.codeName = codeName
		self.codeLocation = codeLocation
		self.isParallel = isParallel
		self.stoppingConditions = stoppingConditions
		self.parameters = parameters
	
	# Methods
	def toXml(self):
		'''Dumps the Module to an XML element.
		
		The element is formatted as follows:
		<Module name="Example">
		  <description>The example module is an example module.</description>
		  <domain>Stellar Dynamics</domain>
		  <codeName>example.py</codeName>
		  <codeLocation>src/amuse/community/example</codeLocation>
		  <isParallel>false</isParallel>
		  <stoppingConditions>TIMEOUT | NUMBER_OF_STEPS | ESCAPER</stoppingConditions>
		  <Parameter name="Parameter 1">
		    ...
		  </Parameter>
		  <Parameter name="Parameter 2">
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
		
		codeName = etree.SubElement(module, "codeName")
		codeName.text = self.codeName
		
		codeLocation = etree.SubElement(module, "codeLocation")
		codeLocation.text = self.codeLocation
		
		isParallel = etree.SubElement(module, "isParallel")
		isParallel.text = str(self.isParallel)  # Convert boolean to string for serialization
		
		stoppingConditions = etree.SubElement(module, "stoppingConditions")
		stoppingConditions.text = self.stoppingConditions
		
		# Iterate through parameters and append them as sub-elements
		for parameter in self.parameters:
			module.append(etree.fromstring(parameter.toXml()))
		
		# Prettify the XML
		uglyXml = xml.dom.minidom.parseString(etree.tostring(module, encoding = "UTF-8"))
		
		return uglyXml.toprettyxml(encoding = "UTF-8")
	
	@staticmethod
	def fromXml(element):
		'''Recreates a Module from its XML specification.
		
		Parameters:
		  element -- A string containing an XML representation of a Module.
		
		Output:
		  A Module whose property values are specified by the given XML element.'''
		
		# Parse Module from XML
		moduleElement = etree.fromstring(element)
		
		# Extract Module's properties from XML attributes and sub-elements
		name = moduleElement.get("name")
		
		description        = moduleElement.find("description").text.strip()
		domain             = moduleElement.find("domain").text.strip()
		codeName           = moduleElement.find("codeName").text.strip()
		codeLocation       = moduleElement.find("codeLocation").text.strip()
		isParallel         = eval(moduleElement.find("isParallel").text.strip())  # Evaluate string as boolean
		stoppingConditions = moduleElement.find("stoppingConditions").text.strip()
		
		# Create the Module
		module = Module(name, description, domain, codeName, codeLocation, isParallel, stoppingConditions, [])
		
		# Iterate through Parameter elements and add Parameters to the Module
		for parameterElement in moduleElement.findall("Parameter"):
			parameter = Parameter.fromXml(etree.tostring(parameterElement, encoding = "UTF-8"))
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
	
	# Accessors
	def getName(self):
		'''Returns the name of the module.
		
		Output:
		  The full name of the module.'''
		
		return self.name
	
	def setName(self, name):
		'''Updates this module's name to the given argument.
		
		Parameters:
		  name -- A new, full name for this module.'''
		
		self.name = name
	
	def getDescription(self):
		'''Returns this module's descriptive text.
		
		Output:
		  A description of the module's purpose and the calculations it performs.'''
		
		return self.description
	
	def setDescription(self, description):
		'''Updates this module's descriptive text to the given argument.
		
		Parameters:
		  description -- A new description of this module's purpose and calculations performed.'''
		
		self.description = description
	
	def getAstrophysicalDomain(self):
		'''Returns this module's astrophysical domain.
		
		Output:
		  The astrophysical domain into which the module has been sorted.'''
		
		return self.domain
	
	def setAstrophysicalDomain(self, domain):
		'''Updates this module's astrophysical domain.
		
		Parameters:
		  domain -- An astrophysical domain into which this module will be sorted.'''
		
		self.domain = domain
	
	def getCodeName(self):
		'''Returns the name of the module's associated AMUSE class.
		
		Output:
		  The name of the AMUSE class containing this module's code.'''
		
		return self.codeName
	
	def setCodeName(self, codeName):
		'''Updates this module's code reference to the given argument.
		
		Parameters:
		  codeName -- The name of an AMUSE class containing this module's code.'''
		
		self.codeName = codeName
	
	def getCodeLocation(self):
		'''Returns the location of the module's AMUSE code.
		
		Output:
		  The location of the AMUSE code that specifies this module.'''
		
		return self.codeLocation
	
	def setCodeLocation(self, codeLocation):
		'''Updates this module's code location reference to the given argument.
		
		Parameters:
		  codeLocation -- The location of the AMUSE code that defines this module.'''
		
		self.codeLocation = codeLocation
	
	def getParallelism(self):
		'''Returns a boolean indicating whether the module's calculations can be parallelized.
		
		Output:
		  Whether the module's calculations can be parallelized across multiple workers by MPI.'''
		
		return self.isParallel
	
	def setParallelism(self, isParallel):
		'''Sets or clears the parallelism flag for this module.
		
		Parameters:
		  isParallel -- Whether the module's calculations can be parallelized across multiple workers by MPI.'''
		
		self.isParallel = isParallel
	
	def getStoppingConditions(self):
		'''Returns the stopping conditions specified for the module.
		
		Output:
		  The conditions under which this module may stop executing prematurely.'''
		
		return self.isParallel
	
	def setStoppingConditions(self, conds):
		'''Updates this module's stopping conditions to those represented by the given argument.
		
		Parameters:
		  conds -- A bitfield indicating the stopping conditions for this module.'''
		
		self.stoppingConditions = conds
	
	def getParameters(self):
		'''Returns the parameters of this module.
		
		Output:
		  A list of the module's parameters.'''
		
		return self.parameters
	
	def setParameters(self, parameters):
		'''Updates this module's parameter list to the given argument.
		
		Parameters:
		  parameters -- A list of module parameters.'''
		
		self.parameters = parameters
        
    	@property
    	def result(self):
        	'''Returns an instance of the value. Treats result as a value
		rather than a function.'''
		
        	return None

class Parameter:
	'''A parameter to an AMUSE module.
	
	Modules have parameters that may be modified by the user via the
	graphical interface. These parameters are typically specific to the
	module's domain or even to the individual module. The Parameter class is
	a generic class whose type parameter specifies the type of the
	parameter's value (e.g. integer or floating-point). A parameter may be a
	physical quantity, flag, or other value.'''
	
	# Constructor
	def __init__(self, name, description, defaultValue, minValue, maxValue, units):
		'''Initializes a new Parameter with the given instance data.
		
		Parameters:
		  name -- The brief, descriptive name of the parameter.
		  description -- A description of the parameter's meaning and effects.
		  defaultValue -- The parameter's default value.
		  minValue -- A lower bound on the range of valid parameter values.
		  maxValue -- An upper bound on the range of valid parameter values.
		  units -- The physical unit(s) associated with the parameter's value.'''
		
		self.name = name
		self.description = description
		self.defaultValue = defaultValue
		self.minValue = minValue
		self.maxValue = maxValue
		self.units = units
	
	# Methods
	def toXml(self):
		'''Dumps the Parameter to an XML element.
		
		The parameter is formatted as follows:
		<Parameter name="Example">
		  TODO
		</Parameter>
		
		Output:
		  A string containing an XML representation of the Parameter.'''
		
		# Create <Parameter> XML element and set its attributes
		parameter = etree.Element("Parameter", attrib = {"name" : self.name})
		
		# Append sub-elements
		description = etree.SubElement(parameter, "description")
		description.text = self.description
		
		defaultValue = etree.SubElement(parameter, "defaultValue")
		defaultValue.text = str(self.defaultValue)  # Convert integers to strings for serialization
		
		minValue = etree.SubElement(parameter, "minValue")
		minValue.text = str(self.minValue)
		
		maxValue = etree.SubElement(parameter, "maxValue")
		maxValue.text = str(self.maxValue)
		
		parameter.append(etree.fromstring(self.units.toXml()))
		
		# Prettify the XML
		uglyXml = xml.dom.minidom.parseString(etree.tostring(parameter, encoding = "UTF-8"))
		
		return uglyXml.toprettyxml(encoding = "UTF-8")
	
	@staticmethod
	def fromXml(element):
		'''Recreates a Parameter from its XML specification.
		
		Parameters:
		  element -- A string containing an XML representation of a Parameter.
		
		Output:
		  A Parameter whose property values are specified by the given XML element.'''
		
		# Parse Parameter from XML
		parameterElement = etree.fromstring(element)
		
		# Extract Parameter's properties from XML attributes and sub-elements
		name = parameterElement.get("name")
		
		description = parameterElement.find("description").text.strip()
		defaultValue = eval(parameterElement.find("defaultValue").text.strip())  # Evaluate strings as integers
		minValue    = eval(parameterElement.find("minValue").text.strip())
		maxValue    = eval(parameterElement.find("maxValue").text.strip())
		
		# Read Units sub-element into a CompoundUnit instance
		unitsElement = parameterElement.find("Units")
		units        = CompoundUnit.fromXml(etree.tostring(unitsElement, encoding = "UTF-8"))
		
		# Create the Parameter
		parameter = Parameter(name, description, defaultValue, minValue, maxValue, units)
		
		return parameter
	
	# Accessors
	def getName(self):
		'''Returns the name of the parameter.
		
		Output:
		  The brief, descriptive name of the parameter.'''
		
		return self.name
	
	def setName(self, name):
		'''Updates this parameter's name to the given argument.
		
		Parameters:
		  name -- A new name for this parameter.'''
		
		self.name = name
	
	def getDescription(self):
		'''Returns this parameter's descriptive text.
		
		Output:
		  A description of the parameter's meaning and effects.'''
		
		return self.description
	
	def setDescription(self, description):
		'''Updates this parameter's descriptive text to the given argument.
		
		Parameters:
		  description -- A new description for this parameter.'''
		
		self.description = description
	
	def getDefaultValue(self):
		'''Returns the default value for this parameter.
		
		Output:
		  The parameter's default value.'''
		
		return self.defaultValue
	
	def setDefaultValue(self, defaultValue):
		'''Updates this parameter's default value to the given argument.
		
		Parameters:
		  defaultValue -- A new default value for this parameter.'''
		
		self.defaultValue = defaultValue
	
	def getMinValue(self):
		'''Returns the minimal allowed value for this parameter.
		
		Output:
		  The parameter's minimum valid value.'''
		
		return self.minValue
	
	def setMinValue(self, minValue):
		'''Updates this parameter's minimum value to the given argument.
		
		Parameters:
		  minValue -- A new lower bound on this parameter's range of possible values.'''
		
		self.minValue = minValue
	
	def getMaxValue(self, ):
		'''Returns the maximal allowed value for this parameter.
		
		Output:
		  The parameter's maximum valid value.'''
		
		return self.maxValue
	
	def setMaxValue(self, maxValue):
		'''Updates this parameter's maximum value to the given argument.
		
		Parameters:
		  axValue -- A new upper bound on this parameter's range of possible values.'''
		
		self.maxValue = maxValue
	
	def getUnits(self):
		'''Returns an object containing the units associated with this parameter.
		
		Output:
		  An object representing the physical unit(s) associated with the parameter's value.'''
		
		return self.units
	
	def setUnits(self, units):
		'''Updates this parameter's units to the given argument.
		
		Parameters:
		  units -- A new compound physical unit to be associated with this parameter.'''
		
		self.units = units

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
	def toXml(self):
		'''Dumps the CompoundUnit to an XML element.
		
		Output:
		  A string containing an XML representation of the CompoundUnit.'''
		
		# TODO: Implement
		raise NotImplementedError, 'XML serialization of CompoundUnits is NYI.'
	
	@staticmethod
	def fromXml(element):
		'''Recreates a CompoundUnit from its XML specification.
		
		Parameters:
		  element -- A string containing an XML representation of a CompoundUnit.
		
		Output:
		  A CompoundUnit whose property values are specified by the given XML element.'''
		
		# TODO: Implement
		raise NotImplementedError, 'XML deserialization of CompoundUnits is NYI.'
	
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
	
	# Accessors
	def getDescription(self):
		'''Returns a textual description of this combined unit.
		
		Output:
		  A non-abbreviated textual description of the combined physical unit.'''
		
		return self.description
	
	def setDescription(self, description):
		'''Updates this instance's description to the given argument.
		
		Parameters:
		  description -- A new, full description for this compound unit.'''
		
		self.description = description
	
	def getSymbolicDescription(self):
		'''Returns an abbreviated description of this combined unit.
		
		Output:
		  A shorthand textual description of the combined physical unit, using unit abbreviations.'''
		
		return self.symbolicDescription
	
	def setSymbolicDescription(self, symbolicDescription):
		'''Updates this instance's short description to the given argument.
		
		Parameters:
		  symbolicDescription -- A new abbreviated description for this compound unit.'''
		
		self.symbolicDescription = symbolicDescription
	
	def getUnits(self):
		'''Returns the list of units contained in this compound unit.
		
		Output:
		  The list of simple units whose combination is represented by this compound unit.'''
		
		return self.units
	
	def setUnits(self, units):
		'''Updates this instance's list of simple units to the given argument.
		
		Parameters:
		  units -- A list of simple units to which this instance should be updated.'''
		
		self.units = units

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
	def toXml(self):
		'''Dumps the Unit to an XML element.
		
		Output:
		  A string containing an XML representation of the Unit.'''
		
		# TODO: Implement
		raise NotImplementedError, 'XML serialization of Units is NYI.'
	
	@staticmethod
	def fromXml(element):
		'''Recreates a Unit from its XML specification.
		
		Parameters:
		  element -- A string containing an XML representation of a Unit.
		
		Output:
		  A Unit whose property values are specified by the given XML element.'''
		
		# TODO: Implement
		raise NotImplementedError, 'XML deserialization of Units is NYI.'
	
	# Accessors
	def getType(self):
		'''Returns the base type of astrophysical unit represented by this instance.
		
		Output:
		  The base type of astrophysical unit being represented.'''
		
		return self.utype
	
	def setType(self, utype):
		'''Updates this instance's base unit type to the given argument.
		
		Parameters:
		  utype -- A base astrophysical unit to which this instance should be updated.'''
		
		self.utype = utype
	
	def getPrefix(self):
		'''Returns the SI prefix that augments the magnitude of this unit.
		
		Output:
		  The SI prefix that modifies the base unit's order of magnitude.'''
		
		return self.prefix
	
	def setPrefix(self, prefix):
		'''Updates this instance's SI prefix to the given argument.
		
		Parameters:
		  prefix -- An SI prefix that will replace this instance's current SI prefix.'''
		
		self.prefix = prefix
	
	def getExponent(self):
		'''Returns the exponent applied to this unit.
		
		Output:
		  The exponent applied to this unit.'''
		
		return self.exponent
	
	def setExponent(self, exponent):
		'''Updates this instance's exponent to the given argument.
		
		Parameters:
		  exponent -- A new exponent to be applied to this unit.'''
		
		self.exponent = exponent

