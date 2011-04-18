#!/usr/bin/python
#
# EnergyLogging.py
#	Introductory Logging of Time, the Energies, and the Virial Ratio
#	Experiment object where it is updated.
#
# 4/17 - Tim McJilton - created EnergyLogger class.
#
# Team GPUnit - Senior Design 2011
#
from diagnostics.Diagnostic import Diagnostic
import numpy as np
from math import sqrt
def get_kinetic(particles):
#    particles = gravity.particles
#    k = 0.
#    uc = gravity.unit_converter.to_nbody
#    for p in particles:
#        k += 0.5 * uc(p.mass).number * (
#            uc(reduce(lambda x,y: x+y, map(lambda (x,y):x*y,zip(p.velocity,p.velocity)))
#                   )).number

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
class EnergyLogger(Diagnostic):

    def __init__(self) :
        self.name = "Energy Logger File"
        self.conditions = []
        self.fout = open("Energy.log",'w')

    def update(self, time, particles) :
        '''This function needs to be overridden by subclasses'''
        KE = get_kinetic(particles)
        PE = get_potential(particles)
        self.fout.write("Time: %f\n"%time.number)
        self.fout.write("Kinetic Energy: %f\tPotential Energy: %f\t"%(KE,PE))
        self.fout.write("Total Energy: %f\tVirial Ratio: %f\n"%(KE+PE,-2.*KE/PE))
#        print particles
#        self.fout.write("%f %f %f %f %f %f %f"%tuple([time.number]+list(particles[0].position.number)+list(particles[1].position.number)))
        

	def shouldUpdate(state) :
		return True


