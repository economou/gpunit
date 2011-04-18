from PyQt4.QtGui import QMainWindow
from gui.ui_clusterview import Ui_ClusterView

MAX_NODE_COLS = 3
"""Maximum number of columns to display in the node grid view."""

class ClusterView(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_ClusterView()
        self.ui.setupUi(self)

        self.nodes = []
        """List of nodes monitored by this ClusterView window."""

    def addNode(self, node):
        if node not in self.nodes:
            row = len(self.nodes) // MAX_NODE_COLS
            col = len(self.nodes) % MAX_NODE_COLS

            self.nodes.append(node)
            self.ui.gridLayout.addWidget(node, row, col)
            self.update()

    def removeNode(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            self.ui.gridLayout.removeWidget(node)
            self.update()
