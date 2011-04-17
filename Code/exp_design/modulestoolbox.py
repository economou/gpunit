from PyQt4.QtGui import QWidget

from gui.ui_modulestoolbox import Ui_ModulesToolBox

class ModulesToolbox(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.ui = Ui_ModulesToolBox()
        self.ui.setupUi(self)
