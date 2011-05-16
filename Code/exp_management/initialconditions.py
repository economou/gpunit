from PyQt4.QtCore import SIGNAL, SLOT, pyqtSlot, Qt
from PyQt4.QtGui import QListWidgetItem, QInputDialog

from amuse.support.units.units import *
from amuse.support.units.si import *
from amuse.support.data.core import Particle, Particles

from amuse.ext.salpeter import SalpeterIMF 
from amuse.ext.plummer import MakePlummerModel
from amuse.ext.kingmodel import MakeKingModel
from amuse.support.io import write_set_to_file, read_set_from_file

from exp_design.settings import SettingsDialog

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

    def setStoragePath(self, path):
        pass

class MassDistribution(InitialCondition):
    def __init__(self, name):
        InitialCondition.__init__(self, name)

    def getMassList(self):
        pass

    def __reduce__(self):
        return (self.__class__, (self.name,), self.__dict__)

class ParticleDistribution(InitialCondition):
    def __init__(self, name):
        InitialCondition.__init__(self, name)

    def getParticleList(self):
        pass
        
    def __reduce__(self):
        return (self.__class__, (self.name,), self.__dict__)

from exp_design.gui.particlesettings_ui import Ui_ParticleSettingsDialog
from PyQt4.QtGui import QDialog, QTreeWidgetItem, QTreeWidgetItemIterator
from amuse.support.units import units

class CustomParticles(ParticleDistribution):
    def __init__(self, numParticles, particlesPath = None, storageFilename = None):
        ParticleDistribution.__init__(self, "CustomParticles")

        self.dialog = QDialog()
        self.ui = Ui_ParticleSettingsDialog()
        self.ui.setupUi(self.dialog)

        self.dialog.connect(self.ui.addParticleButton, SIGNAL("clicked()"), self.treeAddParticle)
        self.dialog.connect(self.ui.removeParticleButton, SIGNAL("clicked()"), self.treeRemoveParticle)


        if storageFilename is None:
            self.particles = Particles(0)
        else:
            self.particles = read_set_from_file(particlesPath + storageFilename, "hdf5")
            self.numParticles = len(self.particles)

            self.storageFilename = storageFilename
            self.particlesPath = particlesPath

            self.ui.pathText.setText(self.storageFilename)

    def setStoragePath(self, path):
        self.particlesPath = path

    def __reduce__(self):
        write_set_to_file(self.particles, self.particlesPath + self.storageFilename, "hdf5")

        pickleDict = self.__dict__.copy()

        del pickleDict["particles"]
        del pickleDict["dialog"]
        del pickleDict["ui"]

        return (CustomParticles, (self.numParticles, self.particlesPath, self.storageFilename), pickleDict)

    def getParticleList(self):
        return self.particles.copy()

    def __setstate__(self, state):
        self.__dict__ = dict(self.__dict__, **state)

        particles = read_set_from_file(self.particlesPath + self.storageFilename, "hdf5")
        self.particles = Particles(len(particles))
        self.numParticles = len(particles)

        try:
            positionUnit = eval(self.positionUnit)
            massUnit = eval(self.massUnit)
            radiusUnit = eval(self.radiusUnit)
            velUnit = eval(self.velUnit)
        except:
            positionUnit = AU
            massUnit = MSun
            radiusUnit = AU
            velUnit = km/s

        for i in range(len(particles)):
            self.particles[i].position = particles[i].position.as_quantity_in(positionUnit)
            self.particles[i].mass = particles[i].mass.as_quantity_in(massUnit)
            self.particles[i].velocity = particles[i].velocity.as_quantity_in(velUnit)
            self.particles[i].radius = particles[i].radius.as_quantity_in(radiusUnit)

        self.ui.pathText.setText(self.storageFilename)

    @pyqtSlot()
    def treeAddParticle(self):
        item = QTreeWidgetItem(
                ("0.0", "0.0", "0.0", "AU",
                    "0.0", "0.0", "0.0", "km/s",
                    "0.0", "MSun",
                    "0.0", "km"
                    ))
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.ui.particlesTree.addTopLevelItem(item)

    def treeRemoveParticle(self):
        item = self.ui.particlesTree.currentItem()
        index = self.ui.particlesTree.indexFromItem(item)

        self.ui.particlesTree.takeTopLevelItem(index.row())

    def setupDialog(self):
        for particle in self.particles:
            pos = particle.position.number
            vel = particle.velocity.number
            mass = particle.mass.number
            radius = particle.radius.number

            item = QTreeWidgetItem((
                str(pos[0]), str(pos[1]), str(pos[2]), str(particle.position.unit),
                str(vel[0]), str(vel[1]), str(vel[2]), str(particle.velocity.unit),
                str(mass), str(particle.mass.unit),
                str(radius), str(particle.radius.unit)
                ))

            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.ui.particlesTree.addTopLevelItem(item)

    def showSettingsDialog(self):
        self.setupDialog()
        result = self.dialog.exec_()
        self.storageFilename = str(self.ui.pathText.text())

        allGood = False

        if result == QDialog.Accepted:
            allGood = True
            i = 0
            it = QTreeWidgetItemIterator(self.ui.particlesTree)

            newParticles = Particles(self.ui.particlesTree.topLevelItemCount())

            while it.value() is not None:
                posX, pXGood = it.value().data(0, Qt.DisplayRole).toFloat()
                posY, pYGood = it.value().data(1, Qt.DisplayRole).toFloat()
                posZ, pZGood = it.value().data(2, Qt.DisplayRole).toFloat()

                posUnit = str(it.value().data(3, Qt.DisplayRole).toString())
                try:
                    eval(posUnit)
                    posUnitGood = True
                except:
                    posUnitGood = False

                velX, vXGood = it.value().data(4, Qt.DisplayRole).toFloat()
                velY, vYGood = it.value().data(5, Qt.DisplayRole).toFloat()
                velZ, vZGood = it.value().data(6, Qt.DisplayRole).toFloat()

                velUnit = str(it.value().data(7, Qt.DisplayRole).toString())
                try:
                    eval(velUnit)
                    velUnitGood = True
                except:
                    velUnitGood = False

                mass, massGood = it.value().data(8, Qt.DisplayRole).toFloat()

                massUnit = str(it.value().data(9, Qt.DisplayRole).toString())
                try:
                    eval(massUnit)
                    massUnitGood = True
                except:
                    massUnitGood = False

                radius, radiusGood = it.value().data(10, Qt.DisplayRole).toFloat()

                radiusUnit = str(it.value().data(11, Qt.DisplayRole).toString())
                radiusUnitGood = (radiusUnit in units.__dict__)

                checks = (pXGood, pYGood, pZGood, posUnitGood, vXGood, vYGood,
                        vZGood, velUnitGood, massGood, massUnitGood)

                allGood = reduce(lambda x,y: x and y, checks, allGood)

                if allGood:
                    newParticles[i].position = [posX, posY, posZ] | eval(posUnit)
                    newParticles[i].velocity = [velX, velY, velZ] | eval(velUnit)
                    newParticles[i].mass = mass | eval(massUnit)
                    newParticles[i].radius = radius | eval(radiusUnit)

                it += 1
                i += 1

        if(allGood):
            del self.particles
            self.particles = newParticles

            self.positionUnit = posUnit
            self.massUnit = massUnit
            self.radiusUnit = radiusUnit
            self.velUnit = velUnit

            self.numParticles = len(self.particles)

        self.ui.particlesTree.clear()

class SalpeterModel(MassDistribution):
    def __init__(self, numParticles, mass_min = 0.1 | MSun, mass_max = 125 | MSun, alpha = -2.35):
        MassDistribution.__init__(self, "Mass Distribution (Salpeter Model)")

        self.numParticles = numParticles
        self.mass_min = mass_min
        self.mass_max = mass_max
        self.alpha = alpha

        self.settings = SettingsDialog(
                inputs = {"Particles:" : "int:1:"},
                defaults = {"Particles:" : self.numParticles})

    def getMassList(self):
        return SalpeterIMF(self.mass_min, self.mass_max, self.alpha).next_set(self.numParticles)
        
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

    def showSettingsDialog(self):
        results = self.settings.getValues()
        if len(results) > 0:
            self.numParticles= results["Particles:"]

    def __reduce__(self):
        pickleDict = self.__dict__.copy()
        del pickleDict["settings"]

        return (SalpeterModel, (self.numParticles,), pickleDict)

class PlummerModel(ParticleDistribution):
    def __init__(self, numParticles, convert_nbody = None, radius_cutoff = 1.0,
            mass_cutoff = 1.0, do_scale = False, random_state = None):
        ParticleDistribution.__init__(self, "Particle Distribution (Plummer Model)")

        self.numParticles = numParticles
        self.convert_nbody = convert_nbody
        self.radius_cutoff = radius_cutoff
        self.mass_cutoff = mass_cutoff
        self.do_scale = do_scale
        self.random_state = random_state

        self.settings = SettingsDialog(
                inputs = {"Particles:" : "int:1:"},
                defaults = {"Particles:" : self.numParticles})

    def getParticleList(self):
        '''Creates a particle list by making a new Plummer model. Note this will be
        different every time this function is called in case any members have changed'''

        return MakePlummerModel(self.numParticles,self.convert_nbody,
            self.radius_cutoff,self.mass_cutoff,self.do_scale,self.random_state).result

    def showSettingsDialog(self):
        results = self.settings.getValues()
        if len(results) > 0:
            self.numParticles= results["Particles:"]

    def __reduce__(self):
        pickleDict = self.__dict__.copy()
        del pickleDict["settings"]

        return (PlummerModel, (self.numParticles,), pickleDict)

class KingModel(ParticleDistribution):
    def __init__(self, numParticles, W0 = 0.0, convert_nbody = None, do_scale = False, 
            beta = 0.0, seed = None, verbose = False):
        ParticleDistribution.__init__(self, "Particle Distribution (King Model)")

        self.numParticles = numParticles
        self.W0 = W0
        self.convert_nbody = convert_nbody
        self.do_scale = do_scale
        self.beta = beta
        self.seed = seed
        self.verbose = verbose

        self.settings = SettingsDialog(
                inputs = {"Particles:" : "int:1:"},
                defaults = {"Particles:" : self.numParticles})

    def getParticleList(self):
        '''Creates a particle list by making a new Plummer model. Note this will be
        different every time this function is called in case any members have changed'''
        return MakeKingModel(self.numParticles,self.W0,self.convert_nbody,
            self.do_scale,self.beta,self.seed,self.verbose).result

    def enableVerbose(self):
        self.verbose = True

    def disableVerbose(self):
        self.verbose = False

    def showSettingsDialog(self):
        results = self.settings.getValues()
        if len(results) > 0:
            self.numParticles= results["Particles:"]

    def __reduce__(self):
        pickleDict = self.__dict__.copy()
        del pickleDict["settings"]

        return (KingModel, (self.numParticles,self.W0, self.convert_nbody, self.do_scale), pickleDict)
