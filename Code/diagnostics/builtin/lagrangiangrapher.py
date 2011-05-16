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
from amuse.support.units import nbody_system
from diagnostics.diagnostic import Diagnostic
import numpy as np
import matplotlib
if "matplotlib.backends" not in sys.modules:
    matplotlib.use("Qt4Agg")

import pylab
from exp_design.settings import SettingsDialog

#from time import gettime
class LRGraph(Diagnostic):
    '''Abstract Diagnostic class. Objects of subclasses are added to the an
    Experiment object where it is updated.'''

    def __init__(self, 
            name = "Lagrangian Diagnostic",
            XLABEL="", 
            YLABEL ="", 
            TITLE = "", 
            UpdateInterval=30., 
            PlotOption="KE PE TE"
            ):
        Diagnostic.__init__(self, name)
        self.setName(name)
        self.convert_nbody = None
        self.XLABEL = XLABEL
        self.YLABEL = YLABEL
        self.TITLE  = TITLE
        self.UpdateInterval = UpdateInterval
        self.PlotOption = PlotOption

        self.datadict = {
            "t":  [],
            "KE": [],
            "PE": [],
            "TE": [],
            "LR": [],
            "HalfMass": []
            }

        self.settings=SettingsDialog(
            inputs = {
            "LABEL X":"str",
            "LABEL Y":"str",
            "LABEL TITLE" :"str",
            "Update Interval":"float:0:",
            "What to Plot? (KE, PE, TE, LR, HalfMass)":"str"
            },
            defaults = {
            "LABEL Y":self.YLABEL,
            "LABEL X":self.XLABEL,
            "LABEL TITLE" :self.TITLE,
            "Update Interval":self.UpdateInterval,
            "What to Plot? (KE, PE, TE, LR, HalfMass)":self.PlotOption
            }
        
        )

    def __reduce__(self):
        newDict = self.__dict__.copy()
        del newDict["settings"]
        if newDict.has_key("particle_sets"):
            del newDict["particle_sets"]
        if newDict.has_key("parent"):
            del newDict["parent"]
        del newDict["pKE"]
        del newDict["pTE"]
        del newDict["pPE"]
        del newDict["p1"]
        del newDict["p2"]
        del newDict["figure"]
        
        return (self.__class__, (self.name, self.XLABEL, self.YLABEL, self.TITLE, self.UpdateInterval, self.PlotOption), newDict)


    def needsGUI(self):
        return True

    def setupGUI(self, parent):
        self.parent = parent
        self.initialize_graphs()
    def initialize_graphs(self):
            self.figure = pylab.figure(1)
            self.p1   = pylab.subplot(211)
            self.pKE, = pylab.plot(self.datadict["t"],self.datadict["KE"])
            self.pPE, = pylab.plot(self.datadict["t"],self.datadict["PE"])
            self.p2   = pylab.subplot(212)
            self.pTE, = pylab.plot(self.datadict["t"],self.datadict["TE"])
    def redraw(self):
        self.figure = pylab.figure(1)
        self.p1   = pylab.subplot(211)
        self.pKE, = pylab.plot(self.datadict["t"],self.datadict["KE"])
        self.pPE, = pylab.plot(self.datadict["t"],self.datadict["PE"])
        self.p2   = pylab.subplot(212)
        self.pTE, = pylab.plot(self.datadict["t"],self.datadict["TE"])
        pylab.show()


    def cleanup(self):
        self.particle_sets = []

    def showSettingsDialog(self):
        results = self.settings.getValues()
        self.XLABEL = results["LABEL X"]
        self.YLABEL = results["LABEL Y"]
        self.TITLE  = results["LABEL TITLE"]
        
        self.UpdateInterval = results["Update Interval"]
        self.PlotOption = results["What to Plot? (KE, PE, TE, LR, HalfMass)"]
#        if len(results) > 0:
#            self.widget.scaleFactor = results["Scale Factor:"]

    def preRunInitialize(self):
        self.datadict = {
            "t":  [],
            "KE": [],
            "PE": [],
            "TE": [],
            "LR": [],
            "HalfMass": []
            }
        self.particle_sets = []
        acceptable = ["KE", "PE", "TE", "LR", "HalfMass"]
        self.toplot = filter(lambda x: x in acceptable,self.PlotOption.split())
        
        #@todo: Create subsets using already written code
    
    def update(self, time, particles, modules) :
        if self.particle_sets == []:
            massgroups = getKeyMasses(particles.mass)
            self.particle_sets = [particles.select(lambda x:  x <= massgroups[0], ["mass"])]
            for i in range(1,len(massgroups)):
                self.particle_sets .append(particles.select(
                    lambda x: x > massgroups[i-1] and x <= massgroups[i], 
                    ["mass"]
                    ))
            self.particle_sets.append(particles)
        LR = np.asarray(get_lagrangians(self.particle_sets, 10))
        self.datadict["LR"].append(LR[-1,:])
        self.datadict["HalfMass"].append(LR[:,5])
        print LR
        print LR[:,5]
        
        self.parent.diagnosticUpdated.emit()
        
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
        if( (cur_mass/total_mass) > cur_list	):
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
        #	print    np.column_stack([range(len(particles)),np.sum(((particles.position - cmpos).number)**2,1)])
        
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

