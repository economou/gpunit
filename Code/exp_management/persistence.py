import os, shutil
import cPickle

from experiment import Experiment
from exp_gen.CLT import run_experiment

def tryMkdirs(path):
    """Attempts to create a hierarchy of directories, doing nothing if they
    exist."""

    if not os.path.exists(path):
        os.makedirs(path)

def tryRmdir(path):
    """Attempts to remove a directory, doing nothing if it does not exist."""

    if os.path.exists(path):
        shutil.rmtree(path)

class ExperimentStorage:

    @staticmethod
    def load(filename):
        pass

    def __init__(self, name):
        self.runs = 0

        self.base = Experiment(name)

    def setBase(self, base):
        self.base = base
        self.runs = 0

    def save(self, location):
        pass

    def run(self):
        pass

    def reset(self):
        pass


class FileStorage(ExperimentStorage):

    @staticmethod
    def load(filename):
        #storageFile = open(filename, 'r')
        #storage = cPickle.load(storageFile)
        #storageFile.close()
        #return storage
        # First step towards ability to open exp from anywhere...
        basePath = os.path.dirname(filename)
        mainWD = os.getcwd()
        os.chdir(basePath)
        storageFile = open(os.path.basename(filename), 'r')
        storage = cPickle.load(storageFile)
        storageFile.close()
        storage.basePath = basePath
        os.chdir(mainWD)
        return storage

    def save(self):
        mainWD = os.getcwd()
        os.chdir(self.basePath)
        #outFile = open(self.basePath + os.sep + self.base.name + ".exp", 'w')
        self.setPaths(self.base)

        #objectsDir = self.basePath + os.sep + "objects"
        objectsDir = "objects"
        tryMkdirs(objectsDir)
        
        for module in self.base.modules:
            self.base.modulePaths[module] = objectsDir + os.sep + module.name + ".xml"
        
        for init in self.base.initialConditions:
            self.base.initialConditionPaths[init] = objectsDir + os.sep + init.name + ".init"
            init.setStoragePath(objectsDir + os.sep)

        for diag in self.base.diagnostics:
            self.base.diagnosticPaths[diag] = objectsDir + os.sep + diag.name + ".diag"
        
        self.base.particlesPath = objectsDir + os.sep + self.base.name + ".particles"
        
        outFile = open(self.base.name + ".exp", 'w')
        cPickle.dump(self, outFile)
        outFile.close()
        os.chdir(mainWD)

    def __init__(self, name, basePath = "."):
        ExperimentStorage.__init__(self, name)

        #self.basePath = basePath
        self.basePath = os.path.abspath(basePath)

    def setPaths(self, experiment):
        if self.runs == 0:
            return
        
        #outputDir = self.basePath + os.sep + str(self.runs)
        outputDir = str(self.runs)

        diagnosticsDir = outputDir + os.sep + "diagnostics"
        #loggingDir = outputDir + os.sep + "logs"

        tryMkdirs(diagnosticsDir)
        #tryMkdirs(loggingDir)

        # Set up filenames for this run's output (diagnostics, logging,
        # particles etc...)
        for diag in experiment.diagnostics:
            if diag.needsFile():
                diag.setupFile(diagnosticsDir)

        #for logger in experiment.loggers:
        #    experiment.diagnosticPaths[logger] = logger.name + ".logger"
        #    if logger.needsFile():
        #        logger.setupFile(loggingDir)
        

    def run(self):
        mainWD = os.getcwd()
        os.chdir(self.basePath)
        self.runs += 1
        experiment = self.base.copy()

        self.setPaths(experiment)
        result = run_experiment(experiment)
        self.save()

        for diagnostic in experiment.diagnostics:
            diagnostic.cleanup()
        
        os.chdir(mainWD)
        
        return result

    def reset(self):
        for run in range(self.runs):
            runPath = self.basePath + os.sep + str(run)
            tryRmdir(runPath)

        self.runs = 0
