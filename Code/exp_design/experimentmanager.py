#
# experimentmanager.py
#
# Gabriel Schwartz
# 2/11
#
# Team GPUnit - Senior Design 2011
#

import sys, os

from amuse.support.units.si import *
from amuse.support.units.units import *

from PyQt4.QtGui import QMainWindow, QFileDialog, QInputDialog, QMessageBox, QLineEdit
from PyQt4.QtCore import Qt, pyqtSlot, pyqtSignal, QThread

from exp_management.experiment import Experiment
from exp_management.persistence import FileStorage
from exp_gen.CLT import run_experiment
from gui.experimentmanager_ui import Ui_ExperimentManager

from moduleeditor import ModuleEditor
from clusterview import ClusterView
from node import Node

class ExperimentManager(QMainWindow):
    """The experiment manager implements the logic that handles actions
    performed by the user in the GUI."""

    # These must be declared here in the class body and not in __init__.
    diagnosticUpdated = pyqtSignal()
    runComplete = pyqtSignal()

    def __init__(self, filename = None, parent = None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_ExperimentManager()
        """GUI Implementation"""

        self.ui.setupUi(self)

        self.moduleEditor = ModuleEditor(self)
        self.clusterView = ClusterView(self)

        # TODO: replace with real networking.
        for i in range(30):
            self.clusterView.addNode(Node(self.clusterView, "Node "+ str(i)))

        if filename is not None:
            self.enableUI()
            self.storage = FileStorage.load(filename)
            self.experiment = self.storage.base
            self.updateUiFromExperiment()
        else:
            self.experiment = Experiment()
            self.disableUI()

        self.dirty = False
        self.isRunning = False

        self.diagnosticUpdated.connect(self.redrawDiagnosticWindows)
        self.runComplete.connect(self.runCompleted)

    @pyqtSlot()
    def touch(self):
        """Sets the dirty flag to true, used whenever a piece of data is
        modified."""
        self.dirty = True

    def showDirtySaveBox(self):
        box = QMessageBox()
        box.setText("The experiment has unsaved changes.")
        box.setInformativeText("Do you want to save them?")
        box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        box.setDefaultButton(QMessageBox.Save)
        box.setIcon(QMessageBox.Warning)
        decision = box.exec_()

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
        if self.dirty:
            success = self.showDirtySaveBox()
            if not success:
                return

        basePath = str(QFileDialog.getExistingDirectory(self, "New experiment storage path:"))
        if basePath == "":
            return

        name, accepted = QInputDialog.getText( self, "Experiment Name", "New experiment name:")
        if not accepted:
            return

        name = str(name)

        self.resetUI()
        self.enableUI()

        self.storage = FileStorage(name, basePath)
        self.experiment = self.storage.base

        self.ui.nameText.setText(name)

    @pyqtSlot()
    def openExperiment(self):
        if self.dirty:
            success = self.showDirtySaveBox()
            if not success:
                return

        filename = str(QFileDialog.getOpenFileName(self, "Open experiment..."))

        if filename == "":
            return False

        try:
            self.enableUI()

            self.storage = FileStorage.load(filename)
            self.experiment = self.storage.base
            self.updateUiFromExperiment()
            self.dirty = False
            return True
        except (AttributeError, IOError) as err:
            QMessageBox.critical(self, "Error Opening", "There was an error opening\n\n" + filename + "\n\nError:\n\n" + str(err),
                    )
            self.resetUI()
            self.disableUI()
            return False

    @pyqtSlot()
    def saveExperiment(self):
        try:
            self.storage.save()
            self.dirty = False
            return True
        except (AttributeError, IOError) as err:
            QMessageBox.critical(self, "Error Saving", "There was an error saving the experiment.\nError:\n\n" + str(err),
                    )
            return False

    def closeEvent(self, event):
        if self.dirty:
            success = self.showDirtySaveBox()
            if not success:
                event.ignore()
                return

        event.accept()

    @pyqtSlot()
    def showClusterView(self):
        if not self.clusterView.isVisible():
            self.clusterView.show()

    @pyqtSlot()
    def showModuleEditor(self):
        if not self.moduleEditor.isVisible():
            self.moduleEditor.show()

    def enableUI(self):
        self.ui.centralWidget.setEnabled(True)
        self.ui.menuRun.setEnabled(True)

    def disableUI(self):
        self.ui.centralWidget.setEnabled(False)
        self.ui.menuRun.setEnabled(False)

    def resetUI(self):
        self.ui.initCondList.clear()
        self.ui.moduleList.clear()
        self.ui.diagnosticList.clear()
        #self.ui.loggerList.clear()

        self.ui.nameText.setText("")

        self.ui.startBox.setValue(0.0)
        self.ui.stopBox.setValue(0.0)
        self.ui.stepBox.setValue(0.0)

        self.ui.modulesToolbox.resetUI()
        self.clusterView.resetUI()
        self.moduleEditor.resetUI()

        self.dirty = False

    def updateUiFromExperiment(self):
        self.resetUI()
        self.ui.nameText.setText(self.experiment.name)

        for module in self.experiment.modules:
            moduleList = self.ui.modulesToolbox.ui.moduleList

            self.ui.moduleList.addItem(module)
            matches = moduleList.findItems(module.name, Qt.MatchExactly)
            if len(matches) > 0:
                moduleList.setCurrentItem(matches[0])
                moduleList.takeItem(moduleList.currentRow())

        for initCond in self.experiment.initialConditions:
            initCondList = self.ui.modulesToolbox.ui.initCondList

            self.ui.initCondList.addItem(initCond)
            matches = initCondList.findItems(initCond.name, Qt.MatchExactly)
            if len(matches) > 0:
                initCondList.setCurrentItem(matches[0])
                initCondList.takeItem(initCondList.currentRow())

        for diagnostic in self.experiment.diagnostics:
            diagnosticList = self.ui.diagnosticsToolbox.ui.diagnosticList

            self.ui.diagnosticList.addItem(diagnostic)
            matches = diagnosticList.findItems(diagnostic.name, Qt.MatchExactly)
            if len(matches) > 0:
                diagnosticList.setCurrentItem(matches[0])
                diagnosticList.takeItem(diagnosticList.currentRow())

        self.ui.startBox.setValue(self.experiment.startTime.number)
        self.ui.stopBox.setValue(self.experiment.stopTime.number)
        self.ui.stepBox.setValue(self.experiment.timeStep.number)

        unitString = str(self.experiment.timeUnit.unit)

        self.ui.unitsText.setText(str(self.experiment.timeUnit))

    #
    # GUI Change Handler Slots
    #

    @pyqtSlot()
    def addInitCondition(self, initCond):
        self.experiment.addInitialCondition(initCond)
        self.ui.initCondList.addItem(initCond)
        self.touch()

    @pyqtSlot()
    def removeInitCondition(self):
        initCond = self.ui.initCondList.takeItem(self.ui.initCondList.currentRow())

        self.experiment.removeInitCondition(initCond)
        self.ui.modulesToolbox.ui.initCondList.addItem(initCond)
        self.touch()

    @pyqtSlot()
    def addModule(self, module):
        self.ui.moduleList.addItem(module)
        self.experiment.modules.append(module)
        self.touch()

    @pyqtSlot()
    def removeModule(self):
        module = self.ui.moduleList.takeItem(self.ui.moduleList.currentRow())

        self.experiment.modules.remove(module)
        self.ui.modulesToolbox.ui.moduleList.addItem(module)
        self.touch()

    @pyqtSlot()
    def addDiagnostic(self, diagnostic):
        # TODO: this will be replaced by a query to the parent hierarchy
        self.experiment.addDiagnostic(diagnostic)
        self.ui.diagnosticList.addItem(diagnostic)
        self.touch()

    @pyqtSlot()
    def removeDiagnostic(self):
        diagnostic = self.ui.diagnosticList.takeItem(self.ui.diagnosticList.currentRow())

        self.experiment.removeDiagnostic(diagnostic)
        self.ui.diagnosticsToolbox.ui.diagnosticList.addItem(diagnostic)
        self.touch()

    @pyqtSlot()
    def addLogger(self, logger):
        self.experiment.addLogger(logger)
        self.ui.loggerList.addItem(logger)
        self.touch()

    @pyqtSlot()
    def removeLogger(self):
        logger = self.ui.loggerList.takeItem(self.ui.loggerList.currentRow())

        self.experiment.removeLogger(logger)
        self.ui.diagnosticsToolbox.ui.loggerList.addItem(logger)
        self.touch()

    @pyqtSlot()
    def nameChanged(self):
        newName = str(self.ui.nameText.text())
        if newName != "":
            self.experiment.name = newName
            self.touch()
        else:
            self.ui.nameText.setText(self.experiment.name)

    @pyqtSlot()
    def initCondSettings(self, index = None):
        if index is not None:
            initCond = self.ui.initCondList.item(index.row())
            initCond.showSettingsDialog()
        else:
            self.ui.initCondList.currentItem().showSettingsDialog()

    @pyqtSlot()
    def moduleSettings(self, index = None):
        if index is not None:
            module = self.ui.moduleList.item(index.row())
            module.showSettingsDialog()
        else:
            self.ui.moduleList.currentItem().showSettingsDialog()

    @pyqtSlot()
    def startChanged(self):
        try:
            self.experiment.startTime = (self.ui.startBox.value() |
                    self.experiment.timeUnit)
            self.touch()
        except ValueError:
            self.ui.startBox.setValue(self.experiment.startTime.number)

    @pyqtSlot()
    def stopChanged(self):
        try:
            self.experiment.stopTime = (self.ui.stopBox.value() |
                    self.experiment.timeUnit)
            self.touch()
        except ValueError:
            self.ui.stopBox.setValue(self.experiment.stopTime.number)

    @pyqtSlot()
    def stepChanged(self):
        try:
            self.experiment.timeStep = (self.ui.stepBox.value() |
                    self.experiment.timeUnit)
            self.touch()
        except ValueError:
            self.ui.stepBox.setValue(self.experiment.timeStep.number)

    @pyqtSlot()
    def unitChanged(self):
        try:
            unit = eval(str(self.ui.unitsText.text()))
            self.experiment.timeUnit = unit
            self.touch()
        except (RuntimeError, NameError, AttributeError, SyntaxError):
            self.ui.unitsText.setText(str(self.experiment.timeUnit))

    #
    # Experiment Running Methods and Classes
    #

    @pyqtSlot()
    def redrawDiagnosticWindows(self):
        for diagnostic in self.experiment.diagnostics:
            if diagnostic.needsGUI():
                diagnostic.redraw()

    @pyqtSlot()
    def runCompleted(self):
        for diagnostic in self.experiment.diagnostics:
            if diagnostic.needsGUI():
                diagnostic.cleanup()

        self.isRunning = False
        self.enableUI()

    @pyqtSlot()
    def runExperiment(self):
        """Spawns a thread to run the experiment.""" 

        if self.isRunning:
            return

        self.isRunning = True
        self.disableUI()

        try:
            del self.runner
        except AttributeError:
            pass

        self.runner = ExperimentRunner(self.experiment, self)
        self.runner.start()

class ExperimentRunner(QThread):
    """A custom thread class used to run the experiment while the GUI renders
    itself."""

    def __init__(self, experiment, parent):
        QThread.__init__(self, parent)
        self.experiment = experiment

        for diagnostic in self.experiment.diagnostics:
            if diagnostic.needsGUI():
                diagnostic.setupGUI(parent)

    def run(self):
        """Runs the experiment and then signals the GUI that the run
        finished."""

        #try:
        self.storage.run()
        #except:
        #    # TODO: use GUI signals here to show a box.
        #    print "ERROR RUNNING EXPERIMENT. TODO: SIGNAL GUI HERE."
        self.parent().runComplete.emit()
