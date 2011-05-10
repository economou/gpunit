from PyQt4.QtCore import pyqtSlot, SIGNAL, SLOT
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
            self.connect(condBox, SIGNAL("stateChanged(int)"), self.stopCondChanged)

        self.dirty = False
        self.ignoreUIChange = False

        self.module = None
        self.resetUI()
        self.disableUI()

    @pyqtSlot()
    def touch(self):
        """Sets the dirty flag to true, used whenever a piece of data is
        modified."""
        self.dirty = True

    def closeEvent(self, event):
        if self.dirty:
            success = self.showDirtySaveBox()
            if not success:
                event.ignore()
                return

        self.resetUI()
        self.disableUI()
        self.module = None
        event.accept()

    @pyqtSlot()
    def setDirty(self):
        """Sets the dirty flag to true, used whenever a piece of data is
        modified."""
        self.dirty = True

    def showDirtySaveBox(self):
        box = QMessageBox()
        box.setText("The module has unsaved changes.")
        box.setInformativeText("Do you want to save them?")
        box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        box.setDefaultButton(QMessageBox.Save)
        box.setIcon(QMessageBox.Warning)
        decision = box.exec_()

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
            self.module = module.Module.fromFile(filename)
            self.enableUI()
            self.updateUiFromModule()
            self.dirty = False
            return True
        except (AttributeError, IOError) as err:
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

        self.ignoreUIChange = True

        self.ui.moduleNameText.setText(self.module.name)
        self.ui.descriptionText.setPlainText(self.module.description)
        self.ui.domainCombo.setCurrentIndex(
                self.ui.domainCombo.findText(self.module.domain))

        self.ui.classNameText.setText(self.module.className)
        self.ui.codeLocationText.setText(self.module.codeLocation)

        self.ui.parallelCheck.setChecked(self.module.isParallel)

        for cond in module.StoppingConditions:
            if self.module.stoppingConditions & module.StoppingConditions[cond]:
                self.checkboxMap[cond].setChecked(True)

        self.ignoreUIChange = False

    def enableUI(self):
        self.ui.centralWidget.setEnabled(True)

        for box in self.checkboxMap.values():
            box.setEnabled(True)

    def disableUI(self):
        self.ui.centralWidget.setEnabled(False)

        for box in self.checkboxMap.values():
            box.setEnabled(False)

    def resetUI(self):
        self.ignoreUIChange = True

        self.ui.moduleNameText.setText("")
        self.ui.descriptionText.setPlainText("")
        self.ui.classNameText.setText("")
        self.ui.codeLocationText.setText("")

        for box in self.checkboxMap.values():
            continue
            #box.setChecked(False)

        self.ignoreUIChange = False

    @pyqtSlot()
    def nameChanged(self):
        if self.ignoreUIChange:
            return

        self.module.name = str(self.ui.moduleNameText.text())
        self.touch()

    @pyqtSlot()
    def descriptionChanged(self):
        if self.ignoreUIChange:
            return

        self.module.description = str(self.ui.descriptionText.document().toPlainText())
        self.touch()

    @pyqtSlot()
    def classNameChanged(self):
        if self.ignoreUIChange:
            return

        self.module.className = str(self.ui.classNameText.text())
        self.touch()

    @pyqtSlot()
    def codeLocationChanged(self):
        if self.ignoreUIChange:
            return

        self.module.codeLocation = str(self.ui.codeLocationText.text())
        self.touch()

    @pyqtSlot()
    def stopCondChanged(self):
        if self.ignoreUIChange:
            return

        newCond = 0
        for name in self.checkboxMap:
            if self.checkboxMap[name].isChecked():
                newCond = (newCond | module.StoppingConditions[name])

        self.module.stoppingConditions = newCond
        self.touch()

    @pyqtSlot()
    def isParallelChanged(self):
        if self.ignoreUIChange:
            return

        self.module.isParallel = str(self.ui.parallelCheck.isChecked())
        self.touch()
