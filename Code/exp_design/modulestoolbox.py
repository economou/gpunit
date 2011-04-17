from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QWidget

from exp_management.PlummerModel import PlummerModel
from gui.ui_modulestoolbox import Ui_ModulesToolBox

class ModulesToolbox(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.ui = Ui_ModulesToolBox()
        self.ui.setupUi(self)

    @pyqtSlot()
    def test(self, item, i):
        print "item:", item.text()
        if i is not None:
            print i.text()
        print

        item.addChild(PlummerModel(32))

    @pyqtSlot()
    def addButtonClicked(self):
        pass
        #self.emit(itemAdded, self.ui.
