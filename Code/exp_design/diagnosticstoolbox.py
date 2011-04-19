from PyQt4.QtCore import pyqtSlot, SIGNAL
from PyQt4.QtGui import QWidget

from diagnostics.builtin.gldiagnostic import *
from diagnostics.builtin.energydiagnostic import *

from gui.diagnosticstoolbox_ui import Ui_DiagnosticsToolBox

diagnostics = (
        OpenGLDiagnostic,
        EnergyDiagnostic,
        )

class DiagnosticsToolbox(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.ui = Ui_DiagnosticsToolBox()
        self.ui.setupUi(self)
        self.resetUi()

    def resetUi(self):
        self.ui.diagnosticList.clear()
        self.ui.loggerList.clear()

        for diag in diagnostics:
            self.ui.diagnosticList.addItem(diag())

    @pyqtSlot()
    def addDiagnostic(self):
        diagnostic = self.ui.diagnosticList.takeItem(self.ui.diagnosticList.currentRow())
        self.emit(SIGNAL("diagnosticAdded(PyQt_PyObject)"), diagnostic)

    @pyqtSlot()
    def addLogger(self):
        logger = self.ui.loggerList.takeItem(self.ui.loggerList.currentRow())
        self.emit(SIGNAL("loggerAdded(PyQt_PyObject)"), initCond)
