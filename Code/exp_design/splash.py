from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSlot

from gui.splash_ui import Ui_SplashScreen

SPLASH_MAIN = 0
SPLASH_NEW = 1
SPLASH_OPEN = 2
SPLASH_QUIT = 3

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

    @pyqtSlot()
    def main(self):
        self.choice = SPLASH_MAIN
        self.accept()

    def getChoice(self):
        self.exec_()
        self.close()
        return self.choice
