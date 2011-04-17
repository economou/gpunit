#!/usr/bin/python
import sys

from PyQt4.QtGui import QApplication
from experimentmanager import ExperimentManager

if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = ExperimentManager()
    w.show()

    exit(a.exec_())
