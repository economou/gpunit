#
# InitialCondition.py
#    Base class for initial condition objects.
#
# Gabriel Schwartz
# 4/11
#
# Team GPUnit - Senior Design 2011
#
#

from PyQt4.QtGui import QListWidgetItem 

class InitialCondition(QListWidgetItem):
    def __init__(self, name):
        QListWidgetItem.__init__(self)

        self.name = name
        self.setText(self.name)

    def setName(self, name):
        self.name = name
        self.setText(self.name)

class MassDistribution(InitialCondition):
    pass

class ParticleDistribution(InitialCondition):
    pass
