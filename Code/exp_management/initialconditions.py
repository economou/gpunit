from PyQt4.QtCore import SIGNAL, SLOT, pyqtSlot, Qt
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QDialog, QTreeWidgetItem, QTreeWidgetItemIterator

from amuse.support.units import units
from amuse.support.units.units import *
from amuse.support.units.si import *
from amuse.support.data.core import Particle, Particles

from amuse.ext.salpeter import SalpeterIMF 
from amuse.ext.plummer import MakePlummerModel
from amuse.ext.kingmodel import MakeKingModel

from amuse.support.io import write_set_to_file, read_set_from_file

from exp_design.gui.particlesettings_ui import Ui_ParticleSettingsDialog
from exp_design.gui.pairmodel_ui import Ui_PairedSettingsDialog
from exp_design.settings import SettingsDialog

class InitialCondition:
    def __init__(self, name):
        self.name = name

    def setName(self, name):
        self.name = name

    def showSettingsDialog(self):
        pass

    def setStoragePath(self, path):
        pass

    def __str__(self):
        return self.name

    def copy(self):
        pass

class MassDistribution(InitialCondition):
    def __init__(self, name):
        InitialCondition.__init__(self, name)

    def getMassList(self):
        pass

class PositionDistribution(InitialCondition):
    def __init__(self, name):
        InitialCondition.__init__(self, name)

    def getPositionList(self):
        pass

class ParticleDistribution(InitialCondition):
    def __init__(self, name):
        InitialCondition.__init__(self, name)

    def getParticleList(self):
        pass

class CustomParticles(ParticleDistribution):
    def __init__(self, numParticles = 10, particlesPath = None, storageFilename = None):
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

    def __getstate__(self):
        write_set_to_file(self.particles, self.particlesPath + self.storageFilename, "hdf5")

        pickleDict = self.__dict__.copy()

        del pickleDict["particles"]
        del pickleDict["dialog"]
        del pickleDict["ui"]

        return pickleDict

    def getParticleList(self):
        return self.particles.copy()

    def __setstate__(self, state):
        self.__dict__ = dict(self.__dict__, **state)

        self.dialog = QDialog()
        self.ui = Ui_ParticleSettingsDialog()
        self.ui.setupUi(self.dialog)

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
    def __init__(self, numParticles = 10, mass_min = 0.1 | MSun, mass_max = 125 | MSun, alpha = -2.35):
        MassDistribution.__init__(self, "SalpeterModel")

        self.numParticles = numParticles
        self.mass_min = mass_min
        self.mass_max = mass_max
        self.alpha = alpha

    def copy(self):
        return SalpeterModel(self.numParticles, self.mass_min, self.mass_max, self.alpha)

    def getMassList(self):
        return SalpeterIMF(self.mass_min, self.mass_max, self.alpha).next_set(self.numParticles)
        
    def showSettingsDialog(self):
        settings = SettingsDialog(
                inputs = {
                    "Particles" : "int:1:",
                    "Minimum Mass (MSun)" : "float:0:",
                    "Maximum Mass (MSun)" : "float:0:",
                    "Alpha" : "float:0:"},

                defaults = {
                    "Particles" : self.numParticles,
                    "Minimum Mass (MSun)" : self.mass_min.number,
                    "Maximum Mass (MSun)" : self.mass_max.number,
                    "Alpha" : self.alpha}
                )

        results = settings.getValues()

        if len(results) > 0:
            self.numParticles= results["Particles"]
            self.mass_min.number = results["Minimum Mass (MSun)"]
            self.mass_max.number = results["Maximum Mass (MSun)"]
            self.alpha = results["Alpha"]

class PlummerModel(PositionDistribution):
    def __init__(self, numParticles = 10, convert_nbody = None, radius_cutoff = 1.0,
            mass_cutoff = 1.0, do_scale = False, random_state = None):
        PositionDistribution.__init__(self, "PlummerModel")

        self.numParticles = numParticles
        self.convert_nbody = convert_nbody
        self.radius_cutoff = radius_cutoff
        self.mass_cutoff = mass_cutoff
        self.do_scale = do_scale
        self.random_state = random_state

    def getPositionList(self):
        '''Creates a particle list by making a new Plummer model. Note this will be
        different every time this function is called in case any members have changed'''

        return MakePlummerModel(self.numParticles,self.convert_nbody,
            self.radius_cutoff,self.mass_cutoff,self.do_scale,self.random_state).result

    def showSettingsDialog(self):
        settings = SettingsDialog(
                inputs = {
                    "Particles" : "int:1:",
                    "Radius Cutoff" : "float:0:",
                    "Mass Cutoff" : "float:0:",
                    "Scale" : "bool"},

                defaults = {
                    "Particles" : self.numParticles,
                    "Radius Cutoff" : self.radius_cutoff,
                    "Mass Cutoff" : self.mass_cutoff,
                    "Scale" : self.do_scale},
                )
        results = settings.getValues()

        if len(results) > 0:
            self.numParticles= results["Particles"]
            self.radius_cutoff = results["Radius Cutoff"]
            self.mass_cutoff = results["Mass Cutoff"]
            self.do_scale = results["Scale"]

    def copy(self):
        return PlummerModel(self.numParticles, self.convert_nbody, self.radius_cutoff, self.mass_cutoff, self.do_scale, self.random_state)

class KingModel(PositionDistribution):
    def __init__(self, numParticles = 10, W0 = 0.0, convert_nbody = None, do_scale = False, 
            beta = 0.0, seed = None, verbose = False):
        PositionDistribution.__init__(self, "KingModel")

        self.numParticles = numParticles
        self.W0 = W0
        self.convert_nbody = convert_nbody
        self.do_scale = do_scale
        self.beta = beta
        self.seed = seed
        self.verbose = verbose

    def copy(self):
        return KingModel(self.numParticles, self.W0, self.convert_nbody, self.do_scale, self.beta, self.seed, self.verbose)

    def getPositionList(self):
        '''Creates a particle list by making a new Plummer model. Note this will be
        different every time this function is called in case any members have changed'''
        return MakeKingModel(self.numParticles,self.W0,self.convert_nbody,
            self.do_scale,self.beta,self.seed,self.verbose).result

    def showSettingsDialog(self):
        settings = SettingsDialog(
                inputs = {
                    "Particles"     : "int:1:",
                    "W0:"           : "float:0:",
                    "beta"          : "float:0:",
                    "Scale"         : "bool",
                    "Verbose"       : "bool",
                    },

                defaults = {
                    "Particles"     : self.numParticles,
                    "W0"            : self.W0,
                    "beta"          : self.beta,
                    "Scale"         : self.do_scale,
                    "Verbose"       : self.verbose}
                )
        results = settings.getValues()

        if len(results) > 0:
            self.numParticles = results["Particles"]
            self.W0 = results["W0:"]
            self.beta = results["beta"]

class PairedModel(ParticleDistribution):
    def __init__(self, numParticles = 10, massModel = None, positionModel = None):
        ParticleDistribution.__init__(self, "PairedModel")

        self.numParticles = numParticles

        self.massModel = massModel
        self.positionModel = positionModel

        if self.massModel is None:
            self.massModel = SalpeterModel()

        if self.positionModel is None:
            self.positionModel = PlummerModel()

        self.dialog = QDialog()
        self.ui = Ui_PairedSettingsDialog()
        self.ui.setupUi(self.dialog)

        self.ui.posSettings.clicked.connect(self.massSettings)
        self.ui.massSettings.clicked.connect(self.positionSettings)

        for name, model in models.items():
            if model == self.__class__:
                continue

            instance = model()
            if isinstance(instance, MassDistribution):
                self.ui.massCombo.addItem(name)
            elif isinstance(instance, PositionDistribution):
                self.ui.posCombo.addItem(name)

        self.massModel.numParticles = self.numParticles
        self.positionModel.numParticles = self.numParticles

    def massSettings(self):
        self.massModel.showSettingsDialog()
        self.massModel.numParticles = self.numParticles

    def positionSettings(self):
        self.positionModel.showSettingsDialog()
        self.positionModel.numParticles = self.numParticles

    def __getstate__(self):
        pickleDict = self.__dict__.copy()
        del pickleDict["dialog"]
        del pickleDict["ui"]

        return pickleDict

    def __setstate__(self, state):
        self.__init__(state["numParticles"], state["massModel"], state["positionModel"])

    def setupDialog(self):
        self.ui.numParticles.setValue(self.numParticles)

        index = self.ui.massCombo.findText(names[self.massModel.__class__])
        if index > -1:
            self.ui.massCombo.setCurrentIndex(index)

        index = self.ui.posCombo.findText(names[self.positionModel.__class__])
        if index > -1:
            self.ui.posCombo.setCurrentIndex(index)

    def showSettingsDialog(self):
        self.setupDialog()
        result = self.dialog.exec_()

        if result == QDialog.Accepted:
            self.numParticles = int(self.ui.numParticles.value())

            mmName = str(self.ui.massCombo.currentText())
            posName = str(self.ui.posCombo.currentText())

            self.massModel = models[mmName]()
            self.positionModel = models[posName]()

            self.massModel.numParticles = self.numParticles
            self.positionModel.numParticles = self.numParticles

    def getParticleList(self):
        self.positionModel.convert_nbody = self.convert_nbody
        self.massModel.convert_nbody = self.convert_nbody

        particles = self.positionModel.getPositionList()
        particles.mass = self.massModel.getMassList()[1]

        return particles

# For GUI implementation use.
models = {
        "Custom Particles" : CustomParticles,
        "Paired Mass + Position Model" : PairedModel,
        "Position Distribution (Plummer Model)" : PlummerModel,
        "Position Distribution (King Model)" : KingModel,
        "Mass Distribution (Salpeter Model)" : SalpeterModel,
        }

names = {}
for key, value in models.items():
    names[value] = key
