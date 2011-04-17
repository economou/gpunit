from PyQt4.QtGui import QMainWindow
from ui_clusterview import Ui_ClusterView

class ClusterView(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_ClusterView()
        self.ui.setupUi(self)

