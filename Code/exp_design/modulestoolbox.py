from PyQt4.QtCore import pyqtSlot, SIGNAL
from PyQt4.QtGui import QWidget

from exp_management.initialconditions import *

from gui.ui_modulestoolbox import Ui_ModulesToolBox

initialConditions = {
        "Plummer" : PlummerModel
        }

class ModulesToolbox(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.ui = Ui_ModulesToolBox()
        self.ui.setupUi(self)

        for initCond in initialConditions.values():
            self.ui.initCondList.addItem(initCond())

    @pyqtSlot()
    def addModule(self):
        self.emit(SIGNAL("moduleAdded(PyQt_PyObject)"), self.ui.moduleList.currentItem())

    @pyqtSlot()
    def addInitCond(self):
        self.emit(SIGNAL("initCondAdded(PyQt_PyObject)"), self.ui.initCondList.currentItem())
