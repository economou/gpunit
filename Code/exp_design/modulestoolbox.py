from PyQt4.QtCore import pyqtSlot, SIGNAL
from PyQt4.QtGui import QWidget

from exp_management.PlummerModel import PlummerModel
from gui.ui_modulestoolbox import Ui_ModulesToolBox

class ModulesToolbox(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.ui = Ui_ModulesToolBox()
        self.ui.setupUi(self)
        self.ui.initCondList.addItem(PlummerModel(32))

    @pyqtSlot()
    def addModule(self):
        self.emit(SIGNAL("moduleAdded"), self.ui.moduleList.currentItem())

    @pyqtSlot()
    def addInitCond(self):
        self.emit(SIGNAL("initCondAdded"), self.ui.initCondList.currentItem())
