from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow, QFileDialog, QMessageBox, QCheckBox
from gui.ui_moduleeditor import Ui_ModuleEditor

from exp_management import Module

STOPCOND_GRID_WIDTH = 3
"""Number of entries per row of checkboxes for stopping conditions."""

class ModuleEditor(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_ModuleEditor()
        self.ui.setupUi(self)

        for domain in sorted(Module.AstrophysicalDomain, key=lambda k: Module.AstrophysicalDomain[k]):
            self.ui.domainCombo.addItem(domain, Module.AstrophysicalDomain[domain])

        numConds = 0
        for condition in sorted(Module.StoppingConditions, key=lambda k: Module.StoppingConditions[k]):
            row = numConds // STOPCOND_GRID_WIDTH
            col = numConds % STOPCOND_GRID_WIDTH
            numConds += 1

            condBox = QCheckBox(condition, self)
            self.ui.stopcondGrid.addWidget(condBox, row, col)

        self.dirty = False
        self.module = None

    @pyqtSlot()
    def setDirty(self):
        """Sets the dirty flag to true, used whenever a piece of data is
        modified."""
        self.dirty = True

    @pyqtSlot()
    def openModule(self):
        pass

    @pyqtSlot()
    def saveModule(self):
        filename = QFileDialog.getSaveFileName(self, "Save module as...")
        if filename == "":
            return

        try:
            #self.module.writeXMLFile(filename)
            self.dirty = False
        except IOError as err:
            QMessageBox.critical(self, "Error Saving", "There was an error writing to\n\n" + filename + "\n\nError:\n\n" + str(err),
                    )
