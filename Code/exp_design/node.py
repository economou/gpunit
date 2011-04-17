from PyQt4.QtGui import QWidget, QPushButton, QVBoxLayout

class Node(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.name = "lolbutton"
        self.ipAddress = ""

        self.cpuUsage = 0.0
        self.freeMemory = 0.0

        self.numCPUs = 0
        self.totalMemory = 0

        self.createChildren()

    def createChildren(self):
        vbox = QVBoxLayout(self)

        self.pbutton = QPushButton(self.name, self)
        vbox.addWidget(self.pbutton)

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
