#!/usr/bin/python
import sys

from PyQt4.QtGui import QApplication, QDialog
from exp_design.experimentmanager import ExperimentManager
from exp_design.splash import SplashScreen, SPLASH_NEW, SPLASH_OPEN, SPLASH_QUIT

if __name__ == "__main__":
    expFilename = None
    if len(sys.argv) > 1:
        expFilename = sys.argv[1]

    app = QApplication(sys.argv)

    if expFilename is None:
        splash = SplashScreen()
        choice = splash.getChoice()

        if choice == SPLASH_QUIT:
            app.quit()
            exit(0)
        else:
            manager = ExperimentManager(initialAction = choice)
    else:
        manager = ExperimentManager(filename = expFilename)

    manager.show()

    exit(app.exec_())
