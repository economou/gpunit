from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSlot

from gui.splash_ui import Ui_SplashScreen

SPLASH_NEW = 0
SPLASH_OPEN = 1
SPLASH_QUIT = 2

class SplashScreen(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        self.choice = SPLASH_QUIT

    @pyqtSlot()
    def newExperiment(self):
        self.choice = SPLASH_NEW
        self.accept()

    @pyqtSlot()
    def openExperiment(self):
        self.choice = SPLASH_OPEN
        self.accept()

    def getChoice(self):
        self.exec_()
        return self.choice
