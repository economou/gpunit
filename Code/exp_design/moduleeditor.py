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
        self.checkboxMap = {}

        for condition in sorted(Module.StoppingConditions, key=lambda k: Module.StoppingConditions[k]):
            row = numConds // STOPCOND_GRID_WIDTH
            col = numConds % STOPCOND_GRID_WIDTH
            numConds += 1

            condBox = QCheckBox(condition, self)
            self.ui.stopcondGrid.addWidget(condBox, row, col)
            self.checkboxMap[condition] = condBox

        self.dirty = False
        self.module = None
        self.resetUI()

    @pyqtSlot()
    def close(self):
        self.resetUI()
        QMainWindow.close(self)

    @pyqtSlot()
    def setDirty(self):
        """Sets the dirty flag to true, used whenever a piece of data is
        modified."""
        self.dirty = True

    @pyqtSlot()
    def openModule(self):
        if self.dirty:
            box = QMessageBox()
            box.setText("The module has unsaved changes.")
            box.setInformativeText("Do you want to save them?")
            box.setStandardButtons(QMessagebox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            box.setDefaultButton(QMessageBox.save)
            decision = box._exec()

            if decision == QMessageBox.Save:
                self.saveModule()
            elif decision == QMessageBox.Cancel:
                return

            self.dirty = False

        filename = QFileDialog.getOpenFileName(self, "Open module...")
        if filename == "":
            return

        try:
            modFile = open(filename, "r")
            xml = ""
            for line in modFile:
                xml += line
            modFile.close()

            self.module = Module.Module.fromXml(xml)
            self.updateUiFromModule()
        except IOError as err:
            QMessageBox.critical(self, "Error Opening", "There was an error opening\n\n" + filename + "\n\nError:\n\n" + str(err),
                    )

    @pyqtSlot()
    def saveModule(self):
        filename = QFileDialog.getSaveFileName(self, "Save module as...")
        if filename == "":
            return

        try:
            #xml = self.module.toXml(filename)
            #modFile = open(filename, "w")
            #modFile.write(xml)
            #modFile.close()
            self.dirty = False
        except IOError as err:
            QMessageBox.critical(self, "Error Saving", "There was an error writing to\n\n" + filename + "\n\nError:\n\n" + str(err),
                    )
    @pyqtSlot()
    def updateUiFromModule(self):
        self.enableUI()

        self.ui.moduleNameText.setText(self.module.name)
        self.ui.descriptionText.setText(self.module.description)
        self.ui.domainCombo.setCurrentIndex(
                self.ui.domainCombo.findText(self.module.domain))

        self.ui.classNameText.setText(self.module.codeName)
        self.ui.codeLocationText.setText(self.module.codeLocation)

        self.ui.parallelCheck.setChecked(self.module.isParallel)

        for cond in Module.StoppingConditions:
            if self.module.stoppingConditions & Module.StoppingConditions[cond]:
                self.checkboxMap[cond].setChecked(True)

    def enableUI(self):
        self.ui.moduleNameText.setEnabled(True)
        self.ui.descriptionText.setEnabled(True)
        self.ui.classNameText.setEnabled(True)
        self.ui.codeLocationText.setEnabled(True)
        self.ui.domainCombo.setEnabled(True)
        self.ui.parallelCheck.setEnabled(True)

        for box in self.checkboxMap.values():
            box.setChecked(False)
            box.setEnabled(True)

    def resetUI(self):
        self.ui.moduleNameText.setText("")
        self.ui.descriptionText.setText("")
        self.ui.classNameText.setText("")
        self.ui.codeLocationText.setText("")

        self.ui.moduleNameText.setEnabled(False)
        self.ui.descriptionText.setEnabled(False)
        self.ui.classNameText.setEnabled(False)
        self.ui.codeLocationText.setEnabled(False)
        self.ui.domainCombo.setEnabled(False)
        self.ui.parallelCheck.setEnabled(False)

        for box in self.checkboxMap.values():
            box.setChecked(False)
            box.setEnabled(False)
