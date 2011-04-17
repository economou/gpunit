#
# PlummerModel.py
#    Class holding a Plummer Model for particle distribution.
#
# Andrew Sherman
# 3/11
#
# Team GPUnit - Senior Design 2011
#
#

from InitialCondition import InitialCondition
from amuse.ext.plummer import MakePlummerModel

class PlummerModel(ParticleDistribution):

    def __init__(self, numParticles, convert_nbody = None, radius_cutoff = None,
            mass_cutoff = None, do_scale = False, random_state = None):
        InitialCondition.__init__(self, "Plummer Model")

        self.numParticles = int(numParticles)
        self.convert_nbody = convert_nbody
        self.radius_cutoff = float(radius_cutoff)
        self.mass_cutoff = float(mass_cutoff)
        self.do_scale = do_scale
        self.random_state = random_state

    def getParticleList(self):
        '''Creates a particle list by making a new Plummer model. Note this will be
        different every time this function is called in case any members have changed'''
        return MakePlummerModel(self.numParticles,self.convert_nbody,
            self.radius_cutoff,self.mass_cutoff,self.do_scale,self.random_state).result

    def getNumParticles(self):
        return self.numParticles

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles

    def getConvertNbody(self):
        return self.convert_nbody

    def setConvertNbody(self, convert_nbody):
        self.convert_nbody = convert_nbody

    def getRadiusCutoff(self):
        return self.radius_cutoff

    def setRadiusCutoff(self, radius_cutoff):
        self.radius_cutoff = radius_cutoff

    def getMassCutoff(self):
        return self.mass_cutoff

    def setMassCutoff(self, mass_cutoff):
        self.mass_cutoff = mass_cutoff

    def getDoScale(self):
        return self.do_scale

    def setDoScale(self, do_scale):
        self.do_scale = do_scale

    def getRandomState(self):
        return self.random_state

    def setRandomState(self, random_state):
        self.random_state = random_state

