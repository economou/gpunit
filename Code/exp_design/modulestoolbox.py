from PyQt4.QtCore import pyqtSlot, SIGNAL
from PyQt4.QtGui import QWidget

from exp_management.initialconditions import *

from gui.ui_modulestoolbox import Ui_ModulesToolBox

initialConditions = {
        "Plummer" : PlummerModel,
        "King" : KingModel,
        "Salpeter" : SalpeterModel,
        }

class ModulesToolbox(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.ui = Ui_ModulesToolBox()
        self.ui.setupUi(self)

        for initCond in initialConditions.values():
            self.ui.initCondList.addItem(initCond(1))

    @pyqtSlot()
    def addModule(self):
        module = self.ui.moduleList.takeItem(self.ui.moduleList.currentRow())
        self.emit(SIGNAL("moduleAdded(PyQt_PyObject)"), module)

    @pyqtSlot()
    def addInitCond(self):
        initCond = self.ui.initCondList.takeItem(self.ui.initCondList.currentRow())
        self.emit(SIGNAL("initCondAdded(PyQt_PyObject)"), initCond)
