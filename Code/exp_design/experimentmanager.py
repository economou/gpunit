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

from ui_experimentmanager import Ui_ExperimentManager
from moduleeditor import ModuleEditor
from clusterview import ClusterView

class tcls(QListWidgetItem):
    def __init__(self, name="TCLS"):
        self.name = name
        QListWidgetItem.__init__(self)
        self.setText(self.name)

class ExperimentManager(QMainWindow):
    """The experiment manager implements the logic that handles actions
    performed by the user in the GUI."""

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        tcl = tcls("LOL")

        self.ui = Ui_ExperimentManager()
        self.ui.setupUi(self)
        self.ui.initCondList.addItem(tcl)

        self.editor = ModuleEditor(self)
        self.clusterView = ClusterView(self)

    @pyqtSlot()
    def newExperiment(self):
        parent = self.parentWidget()
        if parent is None:
            parent = self

        m = ExperimentManager(self)
        m.show()

    @pyqtSlot()
    def openExperiment(self):
        parent = self.parentWidget()
        if parent is None:
            parent = self

        m = ExperimentManager(self)
        m.show()

    @pyqtSlot()
    def saveExperiment(self):
        filename = QFileDialog.getSaveFileName(self, "Save experiment as...")
        try:
            #self.experiment.writeXMLFile(filename)
            raise IOError("TEST ERROR")
        except IOError as err:
            QMessageBox.critical(self, "Error Saving", "There was an error writing to\n\n" + filename + "\n\nError:\n\n" + str(err),
                    )

    def closeEvent(self, event):
        # TODO: Shutdown the network connections here.
        pass

    @pyqtSlot()
    def toggleClusterView(self):
        if not self.clusterView.isVisible():
            self.clusterView.show()
        else:
            self.clusterView.hide()

    @pyqtSlot()
    def toggleModuleEditor(self):
        if not self.editor.isVisible():
            self.editor.show()
        else:
            self.editor.hide()
