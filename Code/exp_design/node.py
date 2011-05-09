from PyQt4.QtGui import QWidget, QPushButton, QProgressBar, QHBoxLayout, QDialog
from PyQt4.QtCore import pyqtSlot

from gui.node_ui import Ui_Node
from gui.nodeinfodialog_ui import Ui_NodeInfoDialog

class Node(QWidget):
    def __init__(self, parent = None, name = ""):
        QWidget.__init__(self, parent)

        self.ui = Ui_Node()
        """GUI Implementation"""

        self.ui.setupUi(self)

        self.infoDialog = QDialog(self)
        self.dialogUi = Ui_NodeInfoDialog()
        self.dialogUi.setupUi(self.infoDialog)

        self.name = str(name)
        self.ui.button.setText(str(name))
        self.ipAddress = ""

        self.ui.usageBar.setValue(0.0)

        self.cpuUsage = 0.0
        self.memoryUsed = 0.0

        self.numCPUs = 1
        self.totalMemory = 1

    @pyqtSlot()
    def showInfo(self):
        self.updateDialog()
        result = self.infoDialog.exec_()

    def updateDialog(self):
        self.dialogUi.nodeNameLabel.setText(str(self.name))
        self.dialogUi.ipLabel.setText(str(self.ipAddress))

        self.dialogUi.memBar.setValue(100.0 * float(self.memoryUsed) / float(self.totalMemory))
        self.dialogUi.usageBar.setValue(self.cpuUsage)
        self.dialogUi.totalMemText.setText(str(int(self.totalMemory)))
        self.dialogUi.numCPUText.setText(str(int(self.numCPUs)))

    def setName(self, name):
        self.name = name;
        self.ui.button.setText(str(self.name))

        self.updateDialog()
        self.update()

    def setUsage(self, usage):
        self.usage = usage

        self.ui.usageBar.setValue(self.cpuUsage)
        self.updateDialog()
        self.update()

    def setNumCPUs(self, cpus):
        self.numCPUs = cpus

        self.updateDialog()
        self.update()

    def setUsedMemory(self, usedmem):
        self.memoryUsed = usedmem

        self.updateDialog()
        self.update()

    def setTotalMemory(self, totalmem):
        self.totalMemory = totalmem

        self.updateDialog()
        self.update()

    def setIpAddress(self, ip):
        self.ipAddress = str(ip)

        if self.name == "":
            self.name = str(ip)

        self.updateDialog()
        self.update()
