#!/usr/bin/python
#
# energydiagnostic.py
#    Introductory diagnostic for Time, the Energies, and the Virial Ratio
#    Experiment object where it is updated.
#
# 4/17 - Tim McJilton - created EnergyDiagnostic class.
#
# Team GPUnit - Senior Design 2011
#

from diagnostics.diagnostic import Diagnostic
import numpy as np
from math import sqrt

def get_kinetic(particles):
    return np.sum(particles.mass*np.sum(particles.velocity*particles.velocity,1)).number/2

def get_potential(particles):
#    particles = gravity.particles
    u = 0.0
 #   uc = gravity.unit_converter.to_nbody
    for p in particles:
        for p2 in particles:
            if p <> p2:
                r2 = (p.x-p2.x)**2 + (p.y-p2.y)**2 + (p.z-p2.z)**2
                r = sqrt(r2.number)
                u += -(p.mass * p2.mass / r).number
    u /= 2
    return u

class EnergyDiagnostic(Diagnostic):
    def __init__(self, name = "EnergyDiagnostic") :
        Diagnostic.__init__(self, name)
        self.fout = None

    def needsFile(self):
        return True

    def setupFile(self, filename = "Energy.log"):
        self.fout = open(filename,'w')

    def cleanup(self):
        self.fout.close()

    def update(self, time, particles) :
        '''This function needs to be overridden by subclasses'''
        KE = get_kinetic(particles)
        PE = get_potential(particles)

        self.fout.write("Time: %f\n"%time.number)
        self.fout.write("Kinetic Energy: %f\tPotential Energy: %f\t"%(KE,PE))
        self.fout.write("Total Energy: %f\tVirial Ratio: %f\n"%(KE+PE,-2.*KE/PE))
