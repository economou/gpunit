#!/usr/bin/python
import sys

from PyQt4.QtGui import QApplication
from exp_design.experimentmanager import ExperimentManager

if __name__ == "__main__":
    expFilename = None
    if len(sys.argv) > 1:
        expFilename = sys.argv[1]

    app = QApplication(sys.argv)
    w = ExperimentManager(filename = expFilename)
    w.show()

    exit(app.exec_())
