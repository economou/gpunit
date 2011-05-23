from PyQt4.QtCore import pyqtSlot, SIGNAL
from PyQt4.QtGui import QWidget

from exp_management.module import Module, ModulePaths
from exp_management.initialconditions import *

from gui.modulestoolbox_ui import Ui_ModulesToolBox

class ModulesToolbox(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.ui = Ui_ModulesToolBox()
        self.ui.setupUi(self)
        self.resetUI()

    def resetUI(self):
        self.ui.initCondList.clear()
        self.ui.moduleList.clear()

        for initCond in models:
            self.ui.initCondList.addItem(initCond())

        for path in ModulePaths.values():
            xml = ""
            xmlFile = open(path, "r")
            for line in xmlFile:
                xml += line
            self.ui.moduleList.addItem(Module.fromXML(xml))

    @pyqtSlot()
    def addModule(self):
        module = self.ui.moduleList.takeItem(self.ui.moduleList.currentRow())
        self.emit(SIGNAL("moduleAdded(PyQt_PyObject)"), module)

    @pyqtSlot()
    def addInitCond(self):
        initCond = self.ui.initCondList.takeItem(self.ui.initCondList.currentRow())
        self.emit(SIGNAL("initCondAdded(PyQt_PyObject)"), initCond)
