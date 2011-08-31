#!/usr/bin/python
#
# snapshotdiagnostic.py
#    Diagnostic for recording particle configurations
#
# 8/2 - Mike Conway - created SnapshotDiagnostic class.
#
# Team GPUnit - Senior Design 2011
#

import os
from amuse.support.io import store
from diagnostics.diagnostic import Diagnostic
from exp_design.settings import SettingsDialog

class SnapshotDiagnostic(Diagnostic):
    def __init__(self, name = "SnapshotDiagnostic", stepsPerSnap = 5) :
        Diagnostic.__init__(self, name)
        self.storage = None
        self.stepsPerSnap = stepsPerSnap
        self.steps = stepsPerSnap

    def needsFile(self):
        return True

    def setupFile(self, dirPath, filename = "Snapshots.hdf5"):
        self.storage = store.StoreHDF(os.path.join(dirPath,filename))

    def cleanup(self):
        self.storage.close()
        self.storage = None
    
    def shouldUpdate(self, time, modules) :
        if self.steps >= self.stepsPerSnap:
            self.steps = 1
            return True
        else:
            self.steps += 1
            return False
    
    def update(self, time, particles, modules) :
        self.storage.store(particles.savepoint(time))
    
    def showSettingsDialog(self):
        settings = SettingsDialog(
                inputs = {"Steps per snapshot:" : "int:1:"},
                defaults = {"Steps per snapshot:" : self.stepsPerSnap})

        results = settings.getValues()
        if len(results) > 0:
            self.stepsPerSnap = results["Steps per snapshot:"]
            self.steps = results["Steps per snapshot:"]

    
