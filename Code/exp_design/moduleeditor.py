from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow, QFileDialog, QMessageBox, QCheckBox
from gui.moduleeditor_ui import Ui_ModuleEditor

from exp_management import module

STOPCOND_GRID_WIDTH = 3
"""Number of entries per row of checkboxes for stopping conditions."""

class ModuleEditor(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_ModuleEditor()
        self.ui.setupUi(self)

        for domain in sorted(module.AstrophysicalDomain, key=lambda k: module.AstrophysicalDomain[k]):
            self.ui.domainCombo.addItem(domain, module.AstrophysicalDomain[domain])

        numConds = 0
        self.checkboxMap = {}

        for condition in sorted(module.StoppingConditions, key=lambda k: module.StoppingConditions[k]):
            row = numConds // STOPCOND_GRID_WIDTH
            col = numConds % STOPCOND_GRID_WIDTH
            numConds += 1

            condBox = QCheckBox(condition, self)
            self.ui.stopcondGrid.addWidget(condBox, row, col)
            self.checkboxMap[condition] = condBox

        self.dirty = False
        self.module = None
        self.resetUI()
        self.disableUI()

    @pyqtSlot()
    def close(self):
        if self.dirty:
            success = self.showDirtySaveBox()
            if not success:
                return

        self.resetUI()
        self.disableUI()
        QMainWindow.close(self)

    @pyqtSlot()
    def setDirty(self):
        """Sets the dirty flag to true, used whenever a piece of data is
        modified."""
        self.dirty = True

    def showDirtySaveBox(self):
        box = QMessageBox()
        box.setText("The module has unsaved changes.")
        box.setInformativeText("Do you want to save them?")
        box.setStandardButtons(QMessagebox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        box.setDefaultButton(QMessageBox.save)
        decision = box._exec()

        if decision == QMessageBox.Save:
            if self.saveModule():
                return True
            else:
                return False
        elif decision == QMessageBox.Cancel:
            return False

        return True

    @pyqtSlot()
    def openModule(self):
        if self.dirty:
            success = showDirtySaveBox()
            if not success:
                return

        filename = QFileDialog.getOpenFileName(self, "Open module...")
        if filename == "":
            return

        try:
            modFile = open(filename, "r")
            xml = ""
            for line in modFile:
                xml += line
            modFile.close()

            self.module = module.Module.fromXML(xml)
            self.enableUI()
            self.updateUiFromModule()
            self.dirty = False
            return True
        except IOError as err:
            QMessageBox.critical(self, "Error Opening", "There was an error opening\n\n" + filename + "\n\nError:\n\n" + str(err),
                    )
            return False

    @pyqtSlot()
    def saveModule(self):
        filename = QFileDialog.getSaveFileName(self, "Save module as...")
        if filename == "":
            return False

        try:
            xml = self.module.toXML()
            modFile = open(filename, "w")
            modFile.write(xml)
            modFile.close()
            self.dirty = False
            return True
        except IOError as err:
            QMessageBox.critical(self, "Error Saving", "There was an error writing to\n\n" + filename + "\n\nError:\n\n" + str(err),
                    )
            return False

    @pyqtSlot()
    def updateUiFromModule(self):
        self.resetUI()

        self.ui.moduleNameText.setText(self.module.name)
        self.ui.descriptionText.setText(self.module.description)
        self.ui.domainCombo.setCurrentIndex(
                self.ui.domainCombo.findText(self.module.domain))

        self.ui.classNameText.setText(self.module.className)
        self.ui.codeLocationText.setText(self.module.codeLocation)

        self.ui.parallelCheck.setChecked(self.module.isParallel)

        for cond in module.StoppingConditions:
            if self.module.stoppingConditions & module.StoppingConditions[cond]:
                self.checkboxMap[cond].setChecked(True)

    def enableUI(self):
        self.ui.centralWidget.setEnabled(True)

        for box in self.checkboxMap.values():
            box.setEnabled(True)

    def disableUI(self):
        self.ui.centralWidget.setEnabled(False)

        for box in self.checkboxMap.values():
            box.setEnabled(False)

    def resetUI(self):
        self.ui.moduleNameText.setText("")
        self.ui.descriptionText.setText("")
        self.ui.classNameText.setText("")
        self.ui.codeLocationText.setText("")

        for box in self.checkboxMap.values():
            box.setChecked(False)
