#
# experimentmanager.py
#
# Gabriel Schwartz
# 2/11
#
# Team GPUnit - Senior Design 2011
#

import sys

from PyQt4.QtGui import QMainWindow, QFileDialog, QInputDialog, QMessageBox, QListWidgetItem
from PyQt4.QtCore import pyqtSlot

from gui.ui_experimentmanager import Ui_ExperimentManager
from moduleeditor import ModuleEditor
from clusterview import ClusterView
from node import Node

from exp_management.initialconditions import PlummerModel
class ExperimentManager(QMainWindow):
    """The experiment manager implements the logic that handles actions
    performed by the user in the GUI."""

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_ExperimentManager()
        """GUI Implementation"""

        self.ui.setupUi(self)

        self.editor = ModuleEditor(self)
        self.clusterView = ClusterView(self)
        for i in range(30):
            self.clusterView.addNode(Node(self.clusterView, "Node "+ str(i)))

        self.experiment = None
        self.dirty = False
        """Set to true if unsaved changes have been made."""

    @pyqtSlot()
    def setDirty(self):
        """Sets the dirty flag to true, used whenever a piece of data is
        modified."""
        self.dirty = True

    @pyqtSlot()
    def newExperiment(self):
        pass

    @pyqtSlot()
    def openExperiment(self):
        pass

    @pyqtSlot()
    def saveExperiment(self):
        filename = QFileDialog.getSaveFileName(self, "Save experiment as...")
        if filename == "":
            return

        try:
            #self.experiment.writeXMLFile(filename)
            self.dirty = False
        except IOError as err:
            QMessageBox.critical(self, "Error Saving", "There was an error writing to\n\n" + filename + "\n\nError:\n\n" + str(err),
                    )

    def closeEvent(self, event):
        # TODO: Shutdown the network connections here.
        pass

    @pyqtSlot()
    def showClusterView(self):
        if not self.clusterView.isVisible():
            self.clusterView.show()

    @pyqtSlot()
    def showModuleEditor(self):
        if not self.editor.isVisible():
            self.editor.show()

    @pyqtSlot()
    def addInitCondition(self, initCond = None):
        self.ui.initCondList.addItem(initCond)

    @pyqtSlot()
    def removeInitCondition(self, initCond = None):
        if initCond is not None:
            return
        else:
            initCond = self.ui.initCondList.takeItem(self.ui.initCondList.currentRow())

            self.experiment.initialConditions.remove(initCond)
            self.ui.modulesToolbox.ui.initCondList.addItem(initCond)

    @pyqtSlot()
    def addModule(self, module = None):
        self.ui.moduleList.addItem(module)
        self.experiment.modules.append(module)

    @pyqtSlot()
    def removeModule(self, module = None):
        if module is not None:
            return
        else:
            module = self.ui.moduleList.takeItem(self.ui.moduleList.currentRow())

            self.experiment.modules.remove(module)
            self.ui.modulesToolbox.ui.moduleList.addItem(module)
