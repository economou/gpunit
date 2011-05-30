#!/usr/bin/python
import sys

from PyQt4.QtGui import QApplication, QDialog
from exp_design.experimentmanager import ExperimentManager
from exp_design.splash import *

if __name__ == "__main__":
    expFilename = None
    if len(sys.argv) > 1:
        expFilename = sys.argv[1]

    app = QApplication(sys.argv)

    choice = SPLASH_MAIN
    if expFilename is None:
        splash = SplashScreen()
        choice = splash.getChoice()

        if choice == SPLASH_QUIT:
            app.quit()
            exit(0)
        else:
            manager = ExperimentManager()
    else:
        manager = ExperimentManager(filename = expFilename)

    manager.show(choice)

    exit(app.exec_())
