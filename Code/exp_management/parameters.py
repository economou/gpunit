from amuse.support.units.si import *
from amuse.support.units.units import *
from amuse.support.units.nbody_system import *

import xml.etree.ElementTree as etree

class Parameter:
    def __init__(self, name, type, default = None, value = None, unit = None, min = None, max = None):
        self.name = name
        self.type = type
        self.default = default
        self.value = value
        self.unit = unit
        self.min = min
        self.max = max

    def appendToXMLElement(self, parametersElement):
        paramElement = etree.SubElement(parametersElement, "parameter")
        paramElement.attrib["name"] = str(self.name)
        paramElement.attrib["type"] = str(self.type)
        
        if self.unit is not None:
            paramElement.attrib["unit"] = str(self.unit)
        if self.default is not None:
            paramElement.attrib["default"] = str(self.default)
        if self.value is not None:
            paramElement.attrib["value"] = str(self.value)

        return paramElement

    def getSettingsEntry(self):
        raise NotImplementedError("Parameters must provide a getSettingsEntry method.")

    @staticmethod
    def paramFromElement(element):
        """Takes an XML parameter element and converts it to a Parameter
        object."""

        attrib = element.attrib
        if "name" not in attrib:
            raise KeyError("Parameter missing required name attribute.")

        if "type" not in attrib:
            raise KeyError("Parameter missing required type attribute.")

        name = attrib["name"]
        typeString = attrib["type"].lower()

        default = attrib["default"] if "default" in attrib else None
        value = attrib["value"] if "value" in attrib else None
        unit = eval(str(attrib["unit"])) if "unit" in attrib else None

        settingValue = None
        param = None

        if typeString == "int":
            rngMin = int(attrib["min"]) if "min" in attrib else ""
            rngMax = int(attrib["max"]) if "max" in attrib else ""


            default = int(default) if default is not None else rngMin
            value = int(value) if value is not None else default

            param = IntParameter(name, default, value, unit, rngMin, rngMax)

        elif typeString == "float":
            rngMin = float(attrib["min"]) if "min" in attrib else ""
            rngMax = float(attrib["max"]) if "max" in attrib else ""

            default = float(default) if default is not None else rngMin
            value = float(value) if value is not None else default

            param = FloatParameter(name, default, value, unit, rngMin, rngMax)
        elif typeString == "bool":
            settingValue = "bool"

            default = eval(default.title()) if default is not None else False
            value = eval(value.title()) if value is not None else default

            param = BoolParameter(name, default, value)
        elif typeString == "enum":
            enums = []

            for enum in element.findall("enum"):
                enums.append(str(enum.text))

            settingValue = enums

            default = default if default is not None else enums[0]
            value = value if value is not None else default

            param = EnumParameter(name, enums, default, value)

        return param

class IntParameter(Parameter):
    def __init__(self, name, default = 0, value = 0, unit = none, min = -2**31+1, max = 2**31-1):
        Parameter.__init__(self, name, "int", default, value, unit, min, max)

    def appendToXMLElement(self, parametersElement):
        paramElement = Parameter.appendToXMLElement(self, parametersElement)
        paramElement.attrib["min"] = str(self.min)
        paramElement.attrib["max"] = str(self.max)

        return paramElement

    def getSettingsEntry(self):
        settingValue = "%s:%s:%s" % (self.type, self.min, self.max)

        #return self.name, self.default, settingValue
        return self.name, self.value, settingValue

class FloatParameter(Parameter):
    def __init__(self, name, default = 0.0, value = 0.0, unit = none, min = -2**31+1, max = 2**31-1):
        Parameter.__init__(self, name, "float", default, value, unit, min, max)

    def appendToXMLElement(self, parametersElement):
        paramElement = Parameter.appendToXMLElement(self, parametersElement)
        paramElement.attrib["min"] = str(self.min)
        paramElement.attrib["max"] = str(self.max)

        return paramElement

    def getSettingsEntry(self):
        settingValue = "%s:%s:%s" % (self.type, self.min, self.max)

        #return self.name, self.default, settingValue
        return self.name, self.value, settingValue

class BoolParameter(Parameter):
    def __init__(self, name, default = False, value = False):
        Parameter.__init__(self, name, "bool", default, value)

    def appendToXMLElement(self, parametersElement):
        return Parameter.appendToXMLElement(self, parametersElement)

    def getSettingsEntry(self):
        #return self.name, self.default, "bool"
        return self.name, self.value, "bool"

class EnumParameter(Parameter):
    def __init__(self, name, choices, default = None, value = None):
        Parameter.__init__(self, name, "enum", default, value)

        self.choices = choices
        if default is None:
            self.default = choices[0]

    def appendToXMLElement(self, parametersElement):
        paramElement = Parameter.appendToXMLElement(self, parametersElement)
        for choice in self.choices:
            enum = etree.SubElement(paramElement, "enum")
            enum.text = choice

        return paramElement

    def getSettingsEntry(self):
        #return self.name, self.default, self.choices
        return self.name, self.value, self.choices
