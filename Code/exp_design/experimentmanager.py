from PyQt4.QtGui import QMainWindow, QFileDialog
from PyQt4.QtCore import pyqtSlot

from ui_experimentmanager import Ui_ExperimentManager
from moduleeditor import ModuleEditor
from clusterview import ClusterView

class ExperimentManager(QMainWindow):
    managers = []
    """Stores a list of opened experiment manager windows."""

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_ExperimentManager()
        self.ui.setupUi(self)

        self.editor = ModuleEditor(self)
        self.clusterView = ClusterView(self)

        ExperimentManager.managers.append(self)

    @pyqtSlot()
    def openManager(self):
        parent = self.parentWidget()
        if parent is None:
            parent = self

        m = ExperimentManager(self)
        m.show()

    @pyqtSlot()
    def saveExperiment(self):
        QFileDialog.getSaveFileName(self, "Save experiment as...")

    def closeEvent(self, event):
        ExperimentManager.managers.remove(self)

        # If this was the last window to close, then close, otherwise ignore
        # the event and hide.
        if len(ExperimentManager.managers) == 0:
            event.accept()
        else:
            event.ignore()
            self.hide()

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
