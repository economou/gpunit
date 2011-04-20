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
from diagnostics.diagnostic import Diagnostic
from PyQt4 import QtCore
import numpy as np
from math import sqrt
import pylab
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
class EnergyGrapher(Diagnostic):

    def __init__(self, name = "Energy Grapher") :
        Diagnostic.__init__(self, name)
        self.name = name
        self.time = []
        self.KE = []
        self.PE = []
        self.TE = []
        self.VR = []
        self.figure = None 
        self.p1   = None #pylab.subplot(211)
        self.pKE  = None #pylab.plot(self.KE)
        self.pPE  = None #pylab.plot(self.PE)
        self.p2   = None #pylab.subplot(212)
        self.pTE  = None #pylab.plot(self.TE)
        self.pVR  = None #pylab.plot(self.VR)
        self.p1min = -1
        self.p1max =  1
        self.p2min = -1
        self.p2max =  1
    def initialize_graphs(self):
            self.figure = pylab.figure(1)
            self.p1   = pylab.subplot(211)
            self.pKE, = pylab.plot(self.time,self.KE)
            self.pPE, = pylab.plot(self.time,self.PE)
            self.p2   = pylab.subplot(212)
            self.pTE, = pylab.plot(self.time,self.TE)
            self.pVR, = pylab.plot(self.time,self.VR)
            self.p1min = min(self.PE[-1]-1,self.KE[-1]-1)
            self.p1max = max(self.PE[-1]+1,self.KE[-1]+1)
            self.p2min = min(self.TE[-1]-1,self.VR[-1]-1)
            self.p2max = max(self.TE[-1]+1,self.VR[-1]+1)
            pylab.show()
        
    def update(self, time, particles) :
        '''This function needs to be overridden by subclasses'''
        
        self.time.append(time.number)
        self.KE.append( get_kinetic( particles ) )
        self.PE.append( get_potential(particles) )
        self.TE.append( self.KE[-1] + self.PE[-1] )
        self.VR.append( self.KE[-1] / self.PE[-1] )
        
        
        if not self.pKE:
            self.initialize_graphs()

        #Add xdata
        self.pKE.set_xdata(self.time)
        self.pPE.set_xdata(self.time)
        self.pTE.set_xdata(self.time)
        self.pVR.set_xdata(self.time)
        #Add ydata
        self.pKE.set_ydata(self.KE)
        self.pPE.set_ydata(self.PE)
        self.pTE.set_ydata(self.TE)
        self.pVR.set_ydata(self.VR)

        self.p1min = min(self.p1min,self.PE[-1],self.KE[-1])
        self.p1max = max(self.p1max,self.PE[-1],self.KE[-1])
        self.p2min = min(self.p1min,self.TE[-1],self.VR[-1])
        self.p2max = max(self.p1max,self.TE[-1],self.VR[-1])
        #Set the Limits
        self.p1.set_xlim(self.time[0],self.time[-1])
        self.p1.set_ylim(self.p1min*1.1,self.p1max*1.1)
        self.p2.set_xlim(self.time[0],self.time[-1])
        self.p2.set_ylim(self.p2min*1.1,self.p2max*1.1)
        
        pylab.draw()
#        self.fout.write("Time: %f\n"%time.number)
#        self.fout.write("Kinetic Energy: %f\tPotential Energy: %f\t"%(KE,PE))
#        self.fout.write("Total Energy: %f\tVirial Ratio: %f\n"%(KE+PE,-2.*KE/PE))
#        print particles
#        self.fout.write("%f %f %f %f %f %f %f"%tuple([time.number]+list(particles[0].position.number)+list(particles[1].position.number)))

    def __reduce__(self):
        newDict = self.__dict__.copy()
        del newDict['figure']
        del newDict['pKE']
        del newDict['pPE']
        del newDict['pTE']
        del newDict['pVR']
        del newDict['p1']
        del newDict['p2']
        return (EnergyGrapher, (self.name, ), newDict)

    def needsGUI(self):
        return False
