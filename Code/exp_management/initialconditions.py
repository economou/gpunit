from PyQt4.QtCore import SIGNAL, SLOT, pyqtSlot, Qt
from PyQt4.QtGui import QListWidgetItem 

from amuse.support.units import units
from amuse.support.data.core import Particles

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

    def showSettingsDialog(self):
        pass

class MassDistribution(InitialCondition):
    def __init__(self, name):
        InitialCondition.__init__(self, name)

    def getMassList(self):
        pass

    def __reduce__(self):
        return (MassDistribution, (self.name,), self.__dict__)

class ParticleDistribution(InitialCondition):
    def __init__(self, name):
        InitialCondition.__init__(self, name)

    def getParticleList(self):
        pass

    def __reduce__(self):
        return (ParticleDistribution, (self.name,), self.__dict__)

from exp_design.gui.ui_particlesettings import Ui_ParticleSettingsDialog
from PyQt4.QtGui import QDialog, QTreeWidgetItem

class CustomParticles(ParticleDistribution):
    def __init__(self, numParticles, particles = None):
        ParticleDistribution.__init__(self, "CustomParticles")

        self.dialog = QDialog()
        self.ui = Ui_ParticleSettingsDialog()
        self.ui.setupUi(self.dialog)

        self.dialog.connect(self.ui.particlesTree, SIGNAL("doubleClicked(QModelIndex)"), self.treeDblClick)

        if particles is None:
            self.particles = Particles(0)
        else:
            self.particles = particles

    @pyqtSlot()
    def treeDblClick(self, index):
        item = self.ui.particlesTree.itemFromIndex(index)
        self.ui.particlesTree.editItem(item, index.column())

    def setupDialog(self):
        item = QTreeWidgetItem(("1", "2", "3", "4", "5", "6"))
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.ui.particlesTree.addTopLevelItem(item)

    def showSettingsDialog(self):
        self.setupDialog()

        original = self.particles.copy()

        result = self.dialog.exec_()
        if result == QDialog.Rejected:
            self.particles = original

class SalpeterModel(MassDistribution):
    def __init__(self, numParticles, mass_min = 0.1 | units.MSun, mass_max = 125 | units.MSun, alpha = -2.35):
        MassDistribution.__init__(self, "SaltpeterModel")

        self.numParticles = numParticles
        self.mass_min = mass_min
        self.mass_max = mass_max
        self.alpha = alpha

    def getMassList(self):
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
        ParticleDistribution.__init__(self, "PlummerModel")

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

class KingModel(ParticleDistribution):

    def __init__(self, number_of_particles, W0 = 0.0, convert_nbody = None, do_scale = False, 
            beta = 0.0, seed = None, verbose = False):
        ParticleDistribution.__init__(self, "KingModel")

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

    def enableVerbose(self):
        self.verbose = True

    def disableVerbose(self):
        self.verbose = False
