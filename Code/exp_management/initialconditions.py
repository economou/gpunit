from PyQt4.QtGui import QListWidgetItem 

from amuse.support.units import units

from amuse.ext.salpeter import SalpeterIMF 
from amuse.ext.plummer import MakePlummerModel
from amuse.ext.kingmodel import MakeKingModel

class InitialCondition(QListWidgetItem):
    def __init__(self, name):
        QListWidgetItem.__init__(self)

        self.name = name
        self.setText(self.name)

    def setName(self, name):
        self.name = name
        self.setText(self.name)

class MassDistribution(InitialCondition):
    def __init__(self, name):
        InitialCondition.__init__(self, name)

    def __reduce__(self):
        return (MassDistribution, (self.name,), self.__dict__)

class ParticleDistribution(InitialCondition):
    def __init__(self, name):
        InitialCondition.__init__(self, name)

    def __reduce__(self):
        return (ParticleDistribution, (self.name,), self.__dict__)

class SalpeterModel(MassDistribution):
    def __init__(self, numParticles, mass_min = 0.1 | units.MSun, mass_max = 125 | units.MSun, alpha = -2.35):
        MassDistribution.__init__(self, "Saltpeter Model")

        self.numParticles = numParticles
        self.mass_min = mass_min
        self.mass_max = mass_max
        self.alpha = alpha

    def getMasses(self):
        return SalpeterIMF(self.mass_min,self.mass_max,alpha).next_set(self.numParticles)
        
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

class PlummerModel(ParticleDistribution):
    def __init__(self, numParticles, convert_nbody = None, radius_cutoff = None,
            mass_cutoff = None, do_scale = False, random_state = None):
        ParticleDistribution.__init__(self, "Plummer Model")

        self.numParticles = numParticles
        self.convert_nbody = convert_nbody
        self.radius_cutoff = radius_cutoff
        self.mass_cutoff = mass_cutoff
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

class KingModel(ParticleDistribution):

    def __init__(self, number_of_particles, W0 = 0.0, convert_nbody = None, do_scale = False, 
            beta = 0.0, seed = None, verbose = False):
        ParticleDistribution.__init__(self, "King Model")

        self.number_of_particles = number_of_particles
        self.W0 = W0
        self.convert_nbody = convert_nbody
        self.do_scale = do_scale
        self.beta = beta
        self.seed = seed
        self.verbose = verbose

    def getParticleList(self):
        '''Creates a particle list by making a new Plummer model. Note this will be
        different every time this function is called in case any members have changed'''
        return MakeKingModel(self.numParticles,self.W0,self.convert_nbody,
            self.do_scale,self.beta,self.seed,self.verbose).result

    def getNumParticles(self):
        return self.numParticles

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles

    def getConvertNbody(self):
        return self.convert_nbody

    def setConvertNbody(self, convert_nbody):
        self.convert_nbody = convert_nbody

    def enableDoScale(self):
        self.do_scale = True

    def disableDoScale(self):
        self.do_scale = False

    def getBeta(self):
        return self.beta

    def setBeta(self, beta):
        self.beta = beta

    def getSeed(self):
        return self.seed

    def setSeed(self, seed):
        self.seed = seed

    def enableVerbose(self):
        self.verbose = True

    def disableVerbose(self):
        self.verbose = False

