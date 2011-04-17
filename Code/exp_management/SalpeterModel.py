#
# SalpeterModel.py
#    Class holding a Salpeter Model for particle mass distribution.
#
# Andrew Sherman
# 3/11
#
# Team GPUnit - Senior Design 2011
#
#

from InitialCondition import MassDistribution
from amuse.ext.salpeter import SalpeterIMF 

class SalpeterModel(MassDistribution):
    def __init__(self, mass_min = 0.1 | units.MSun, mass_max = 125 | units.MSun, alpha = -2.35):
        InitialCondition.__init__(self, "Saltpeter Model")

        self.mass_min = mass_min
        self.mass_max = mass_max
        self.alpha = alpha

    def getScaledMass(self):
        '''Creates a particle list by making a new Plummer model. Note this will be
        different every time this function is called in case any members have changed'''
        return SalpeterIMF(self.mass_min,self.mass_max,alpha)
        
    def getMassMin(self):
        return self.mass_min

    def setMassMin(self, mass_min):
        self.mass_min = mass_min

    def getMassMax(self):
        return self.mass_max

    def setMassMax(self, mass_max):
        self.mass_max = mass_max

    def getAlpha(self):
        return self.alpha

    def setAlpha(self, alpha):
        self.alpha = alpha
