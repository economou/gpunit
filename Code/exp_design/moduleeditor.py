from PyQt4.QtGui import QMainWindow
from ui_moduleeditor import Ui_ModuleEditor

class ModuleEditor(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_ModuleEditor()
        self.ui.setupUi(self)
