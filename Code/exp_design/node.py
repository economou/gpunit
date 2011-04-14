from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QWidget, QPushButton, QProgressBar, QHBoxLayout, QDialog

from ui_nodeinfodialog import Ui_NodeInfoDialog

class Node(QWidget):
    def __init__(self, parent = None, name = "Node"):
        QWidget.__init__(self, parent)

        self.hbox = QHBoxLayout(self)

        self.infoDialog = QDialog(self)
        self.dialogUi = Ui_NodeInfoDialog()
        self.dialogUi.setupUi(self.infoDialog)

        self.name = name
        self.ipAddress = ""

        self.usageBar = QProgressBar(self)
        self.usageBar.setValue(0.0)
        self.button = QPushButton(str(self.name), self)

        self.hbox.addWidget(self.button)
        self.hbox.addWidget(self.usageBar)

        self.connect(self.button, SIGNAL('clicked()'), self.showInfo)

        self.cpuUsage = 0.0
        self.freeMemory = 0.0

        self.numCPUs = 1
        self.totalMemory = 1

    def showInfo(self):
        self.updateDialog()
        self.infoDialog.show()

    def updateDialog(self):
        self.dialogUi.nodeNameLabel.setText(str(self.name))
        self.dialogUi.memBar.setValue(100.0 * float(self.totalMemory - self.freeMemory) / self.totalMemory)
        self.dialogUi.usageBar.setValue(self.cpuUsage)
        self.dialogUi.totalMemText.setText(str(int(self.totalMemory)))
        self.dialogUi.numCPUText.setText(str(int(self.numCPUs)))

    def setName(self, name):
        self.name = name;
        self.button.setText(str(self.name))

        self.updateDialog()
        self.update()

    def setUsage(self, usage):
        self.usage = usage

        self.usageBar.setValue(self.cpuUsage)
        self.updateDialog()
        self.update()

    def setNumCPUs(self, cpus):
        self.numCPUs = cpus

        self.updateDialog()
        self.update()

    def setFreeMemory(self, freemem):
        self.freeMemory = freemem

        self.updateDialog()
        self.update()

    def setTotalMemory(self, totalmem):
        self.totalMemory = totalmem

        self.updateDialog()
        self.update()
