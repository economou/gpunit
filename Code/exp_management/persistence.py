import cPickle

from experiment import Experiment
from exp_gen.CLT import run_experiment

def tryCreateDirs(directory):
    """Attempts to create a hierarchy of directories, doing nothing if they
    exist."""

    path = os.path.dirname(directory)
    if not os.path.exists(path):
        os.makedirs(path)

class ExperimentStorage:

    @staticmethod
    def load(location):
        pass

    def __init__(self, name):
        self.name = name
        self.runs = 0

        self.base = Experiment(name)

    def save(self, location):
        pass

    def run(self):
        pass

import os

def FileStorage(ExperimentStorage):

    @staticmethod
    def load(location:
        storageFile = open(location, 'r')
        storage = cPickle.load(storageFile)
        storageFile.close()
        return storage

    def __init__(self, name, basePath = os.getcwd()):
        ExperimentStorage.__init__(self, name)

        self.basePath = basePath

    def run(self):
        self.runs += 1
        experiment = self.base.copy()

        outputDir = self.basePath + os.sep + str(self.runs)

        diagnosticsDir = outputDir + os.sep + "diagnostics"
        loggingDir = outputDir + os.sep + "logs"
        objectsDir = outputDir + os.sep + "objects"

        tryCreateDirs(diagnosticsDir)
        tryCreateDirs(loggingDir)
        tryCreateDirs(objectsDir)

        # Set up filenames for this run's output (diagnostics, logging,
        # particles etc...)
        experiment.particlesPath = objectsDir + os.sep + experiment.name + ".particles"

        for init in experiment.initialConditions:
            experiment.initialConditionPaths[init] = objectsDir + os.sep + init.name + ".init"

        for diag in experiment.diagnostics:
            experiment.diagnosticPaths[diag] = objectsDir + os.sep + diag.name + ".diag"
            if diag.needsFile():
                diag.setupFile(diagnosticsDir + os.sep + diag.name + ".out")

        for logger in experiment.loggers:
            experiment.diagnosticPaths[logger] = logger.name + ".logger"
            if logger.needsFile():
                logger.setupFile(loggingDir + os.sep + logger.name + ".out")

        run_experiment(experiment)

        for diagnostic in experiment.diagnostics:
            diagnostic.cleanup()
