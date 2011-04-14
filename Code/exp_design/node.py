from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QWidget, QPushButton, QProgressBar, QVBoxLayout, QDialog

from ui_nodeinfodialog import Ui_NodeInfoDialog

class Node(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.vbox = QVBoxLayout(self)

        self.infoDialog = QDialog()
        self.dialogUi = Ui_NodeInfoDialog()
        self.dialogUi.setupUi(self.infoDialog)

        self.name = "TestButton"
        self.ipAddress = ""

        self.dialogUi.nodeNameLabel.setText(self.name)
        self.button = QPushButton(self.name, self)
        self.vbox.addWidget(self.button)

        self.connect(self.button, SIGNAL('clicked()'), self.infoDialog.show)

        self.cpuUsage = 0.0
        self.freeMemory = 0.0

        self.numCPUs = 0
        self.totalMemory = 0

        self.createChildren()

    def createChildren(self):
        pass

    def setName(self, name):
        self.name = name;
        self.update()

    def setUsage(self, usage):
        self.usage = usage
        self.update()

    def setNumCPUs(self, cpus):
        self.numCPUs = cpus
        self.update()

    def setFreeMemory(self, freemem):
        self.freeMemory = freemem
        self.update()

    def setTotalMemory(self, totalmem):
        self.totalMemory = totalmem
        self.update()

    def paintEvent(self, event):
        pass
