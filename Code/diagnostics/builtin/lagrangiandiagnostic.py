#!/usr/bin/python
#
# langrangian_grapher.py
#    Grapher for Langrangian radii and other useful tools
#
# 5/11/11 - Tim McJilton - created LRGraph class.
#
# Team GPUnit - Senior Design 2011
#

import sys
import os

import numpy as np

from amuse.support.units import nbody_system

from diagnostics.diagnostic import Diagnostic
from exp_design.settings import SettingsDialog

class LRDiagnostic(Diagnostic):
    '''Abstract Diagnostic class. Objects of subclasses are added to the an
    Experiment object where it is updated.'''

    def __init__(self, 
            name = "Lagrangian Diagnostic",
            OutputFileName="LagrangianData.log"
            ):

        Diagnostic.__init__(self, name)
        self.setName(name)
        self.filename = OutputFileName
        self.convert_nbody = None
        self.particle_sets = []
        self.directory     = ""

        self.settings=SettingsDialog(
            inputs = {
            "Output File Name":"str"
            },
            defaults = {
            "Output File Name":"LagrangianData.log"
            }
        )
        self.fout = None

    def __reduce__(self):
        newDict = self.__dict__.copy()
        del newDict["settings"]
        if newDict.has_key("particle_sets"):
            del newDict["particle_sets"]
        if newDict.has_key("fout"):
            del newDict["fout"]

        
        return (self.__class__, (self.name, self.filename), newDict)
    def needsFile(self):
        return True
    def setupFile(self, filename = "Lagrangian.log"):
        self.fout = open(os.sep.join([self.directory,self.filename]),'w')#os.sep.join([folder,self.filename]),'w')
        self.fout.write("""#Time=>t\n#Potential Energy=>U\n#Kinetic Energy=>T\n#Seperator=": "\n""")
    def cleanup(self):
        self.particle_sets = []
        self.fout.close()

    def showSettingsDialog(self):
        results = self.settings.getValues()
        if len(results) > 0:
            self.filename = results["Output File Name"]
        

    def preRunInitialize(self):
        self.particle_sets = []
        self.setupFile()
        #@todo: Create subsets using already written code
    
    def update(self, time, particles, modules) :
        if self.particle_sets == []:
            massgroups = getKeyMasses(particles.mass)
            self.particle_sets = [particles.select(lambda x:  x <= massgroups[0], ["mass"])]
            for i in range(1,len(massgroups)):
                self.particle_sets.append(particles.select(
                    lambda x: x > massgroups[i-1] and x <= massgroups[i], 
                    ["mass"]
                    ))
                mass_set = self.convert_nbody.to_nbody(self.particle_sets[-1].mass).number
                self.fout.write("Mass Set: %d\tMin: %f\tMax: %f\tNum: %d\tTotal Mass: %f\n"%(
                    i,
                    mass_set.min(),
                    mass_set.max(),
                    mass_set.size,
                    mass_set.sum()  
                    )
                )
            self.particle_sets.append(particles)
        LR = np.asarray(get_lagrangians(self.particle_sets, 10))
        self.fout.write("Time: %f %s\n"%(time.number,time.unit))
        self.fout.write("Kinetic Energy: %f\tPotential Energy: %f\tTotal Energy: %f\n"%(
            self.convert_nbody.to_nbody(modules[-1].kinetic_energy).number,
            self.convert_nbody.to_nbody(modules[-1].potential_energy).number,
            self.convert_nbody.to_nbody(modules[-1].kinetic_energy+modules[-1].potential_energy).number 
            )
        )
        lr_str = "%f "*10
        
        for i,v in enumerate(LR):
            a = lr_str%tuple(v)
            self.fout.write("%%LR%%%d %s\n"%(i,a))
        #self.fout.flush()
        #self.datadict["LR"].append(LR[-1,:])

        
def getKeyMasses(mass_list):
    '''
    %%%Filtered by Mass with Percent Modifier%%%
    '''
    r_val = []
    mlist = mass_list.sorted()
    total_mass = mlist.sum().number
    cur_list = .1
    cur_mass = 0
    
    for p in mlist:
        cur_mass += p.number

        if((cur_mass/total_mass) > cur_list):
          r_val.append(p)
          cur_list += .1

    return r_val        
        
def get_mcom(particles,	CoMguess = None, cutoff = .9, n_iter = 2 ):
    '''
     Compute the modified center of mass of the system.  Code stolen
     from Starlab and modified to use STL vectors.

     Use center of mass pos and vel as the starting point for
     computing the modified com.

    '''
    nj = len(particles)

    count = n_iter
    cutoff = 1 if cutoff > 1 else cutoff
    count = 0 if cutoff == 1 else count

    j_max = int(cutoff*nj)

    loop = True
    cmpos = CoMguess if CoMguess else particles.center_of_mass()
    while(loop):
        loop = False

        # Set up an array of radii relative to the current center. 
        #Index, Radius
        mrlist = np.column_stack([range(len(particles)),np.sum(((particles.position - cmpos).number)**2,1)])

        # Sort the array by radius.
        mrlist = np.asarray(sorted(list(mrlist),key=lambda x: x[1])) #Sorts by Radii
        psub = particles[map(int,mrlist[:j_max,0])]
        r_sq_maxi = 1/mrlist[j_max][1]

        import sys
        new_pos = np.asarray([0,0,0])
        new_vel = np.asarray([0,0,0])
        r_fac   = 1. - mrlist[:j_max,1]*r_sq_maxi
        r_fac[r_fac < 0] = 0.
        weights = psub.mass.number
        weights = np.asarray( [ i*j for (i,j) in zip(weights,r_fac) ])
        weighted_mass = sum(weights)
        new_pos = np.sum(weights.reshape(j_max,1)*psub.position.number,0)
        new_vel = np.sum(weights.reshape(j_max,1)*particles[map(int,mrlist[:j_max,0])].velocity.number,0)
        if weighted_mass > 0:
            cmpos = list(new_pos/weighted_mass) | particles[0].position.unit
            cmvel = list(new_vel/weighted_mass) | particles[0].position.unit

            count -= 1
            if count >= 0:
                loop = True

    return cmpos 
    
def get_lagrangians(particle_sets, percent_modifier):
    '''
    particles - List of particles used for the iteration
    filter_function(particles,percent_modifier) - Used for filtering specific masses based onsize or range
    percent-modifier - Percent size per iterate. Ex. 10 for 10% iterates

    Returns an PM x PM size list string with appropriate Header

    '''
    comass = get_mcom(particle_sets[-1]) 
    nunits={'mass':nbody_system.mass,'length':nbody_system.length,'time':nbody_system.time}
    r_val = []
    #Setting comass to the the borrowed code for getting center of mass
    getRnoM = lambda p:(p.position-comass).length().number

    pm = percent_modifier*.01 #fltered percentage
    for i,p_set in enumerate(particle_sets):
        r_val.append([]) 
        #Sort the particles by distance from the center
        s_list = sorted(p_set,key=getRnoM)#, reverse=True) Why would I want the largest radius first?

        #Get mass of the particle set:
        #         Note, it is just a number, no units currently. Will need to fix later

        total_mass = sum(map(lambda x: x.mass.number,s_list)) 

        #Set mass counter to 0
        cur_mass = 0

        #Set Current Percent Hunting for to Percent Iterator
        cur_percent = pm

        #Loops across particles in list and prints out the values for when current mass is some percentage.
        #    Lagrangian Radii
        for p in s_list:#cur_mass <= total_mass):
            cur_mass += p.mass.number
            while( cur_mass >= cur_percent * total_mass ):
                r_val[-1].append(getRnoM(p))
                cur_percent += pm

    return r_val
