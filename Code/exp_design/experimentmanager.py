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

from exp_management.Experiment import Experiment

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

        self.experiment = Experiment()
        self.dirty = False
        """Set to true if unsaved changes have been made."""

    @pyqtSlot()
    def setDirty(self):
        """Sets the dirty flag to true, used whenever a piece of data is
        modified."""
        self.dirty = True

    def showDirtySaveBox(self):
        box = QMessageBox()
        box.setText("The experiment has unsaved changes.")
        box.setInformativeText("Do you want to save them?")
        box.setStandardButtons(QMessagebox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        box.setDefaultButton(QMessageBox.save)
        decision = box._exec()

        if decision == QMessageBox.Save:
            if self.saveExperiment():
                return True
            else:
                return False
        elif decision == QMessageBox.Cancel:
            return False

        return True

    @pyqtSlot()
    def newExperiment(self):
        pass

    @pyqtSlot()
    def openExperiment(self):
        if self.dirty:
            success = showDirtySaveBox
            if not success:
                return

        filename = QFileDialog.getOpenFileName(self, "Open experiment...")

        if filename == "":
            return False

        try:
            xml = ""
            expFile = open(filename, "r")
            for line in expFile:
                xml += line

            self.experiment.fromXML(xml)
            self.updateUiFromExperiment()
            self.dirty = False
            return True
        except IOError as err:
            QMessageBox.critical(self, "Error Opening", "There was an error opening\n\n" + filename + "\n\nError:\n\n" + str(err),
                    )
            return False

    @pyqtSlot()
    def saveExperiment(self):
        filename = QFileDialog.getSaveFileName(self, "Save experiment as...")
        if filename == "":
            return False
        
        try:
            self.experiment.writeXMLFile(filename)
            self.dirty = False
            return True
        except IOError as err:
            QMessageBox.critical(self, "Error Saving", "There was an error writing to\n\n" + filename + "\n\nError:\n\n" + str(err),
                    )
            return False

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
    def addInitCondition(self, initCond):
        # TODO: this is wrong
        self.experiment.initialConditions.append((initCond, initCond.name + ".pkl"))
        self.ui.initCondList.addItem(initCond)

    @pyqtSlot()
    def removeInitCondition(self):
        initCond = self.ui.initCondList.takeItem(self.ui.initCondList.currentRow())

        self.experiment.initialConditions.remove(initCond)
        self.ui.modulesToolbox.ui.initCondList.addItem(initCond)

    @pyqtSlot()
    def addModule(self, module):
        self.ui.moduleList.addItem(module)
        self.experiment.modules.append(module)

    @pyqtSlot()
    def removeModule(self):
        module = self.ui.moduleList.takeItem(self.ui.moduleList.currentRow())

        self.experiment.modules.remove(module)
        self.ui.modulesToolbox.ui.moduleList.addItem(module)

    @pyqtSlot()
    def nameChanged(self, newName):
        self.experiment.name = newName

    def updateUiFromExperiment(self):
        self.ui.nameText.setText(self.experiment.name)

        for module in self.experiment.modules:
            self.ui.moduleList.addItem(module)

        for initCond in self.experiment.initialConditions:
            self.ui.initCondList.addItem(initCond[0])

        pass
