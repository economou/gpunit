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

import os

class FileStorage(ExperimentStorage):

    @staticmethod
    def load(filename):
        storageFile = open(filename, 'r')
        storage = cPickle.load(storageFile)
        storageFile.close()
        return storage

    def save(self):
        outFile = open(self.basePath + os.sep + self.base.name + ".exp", 'w')
        self.setPaths(self.base)

        objectsDir = self.basePath + os.sep + "objects"
        tryMkdirs(objectsDir)

        for init in self.base.initialConditions:
            self.base.initialConditionPaths[init] = objectsDir + os.sep + init.name + ".init"
            init.setStoragePath(objectsDir + os.sep)

        for diag in self.base.diagnostics:
            self.base.diagnosticPaths[diag] = objectsDir + os.sep + diag.name + ".diag"

        self.base.particlesPath = objectsDir + os.sep + self.base.name + ".particles"

        cPickle.dump(self, outFile)
        outFile.close()

    def __init__(self, name, basePath = "."):
        ExperimentStorage.__init__(self, name)

        self.basePath = basePath

    def setPaths(self, experiment):
        outputDir = self.basePath + os.sep + str(self.runs)

        diagnosticsDir = outputDir + os.sep + "diagnostics"
        loggingDir = outputDir + os.sep + "logs"

        tryMkdirs(diagnosticsDir)
        tryMkdirs(loggingDir)

        # Set up filenames for this run's output (diagnostics, logging,
        # particles etc...)
        for diag in experiment.diagnostics:
            if diag.needsFile():
                diag.setupFile(diagnosticsDir + os.sep + diag.name + ".out")

        for logger in experiment.loggers:
            experiment.diagnosticPaths[logger] = logger.name + ".logger"
            if logger.needsFile():
                logger.setupFile(loggingDir + os.sep + logger.name + ".out")

    def run(self):
        self.runs += 1
        experiment = self.base.copy()

        self.setPaths(experiment)
        run_experiment(experiment)
        self.save()

        for diagnostic in experiment.diagnostics:
            diagnostic.cleanup()

    def reset(self):
        for run in range(self.runs):
            runPath = self.basePath + os.sep + str(run)
            tryRmdir(runPath)

        self.runs = 0
