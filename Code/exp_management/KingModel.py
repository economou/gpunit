#!/usr/bin/python
#
# KingModel.py
#	Class holding a King Model for particle distribution.
#
# Andrew Sherman
# 3/11
#
# Team GPUnit - Senior Design 2011
#
#

from amuse.ext.kingmodel import MakeKingModel

class KingModel(object):

	def __init__(self, number_of_particles, W0, convert_nbody = None, do_scale = False, 
			beta = 0.0, seed = None, verbose = False):
		self.number_of_particles = number_of_particles
		self.W0 = W0
		self.convert_nbody = convert_nbody
		self.do_scale = do_scale
		self.beta = beta
		self.seed = seed
		self.verbose = verbose

	def getParticleList(self):
		'''Creates a particle list by making a new Plummer model. Note this will be
		different every time this function is called in case any members have changed'''
		return MakeKingModel(self.numParticles,self.W0,self.convert_nbody,
			self.do_scale,self.beta,self.seed,self.verbose).result

	def getNumParticles(self):
		return self.numParticles

	def setNumParticles(self, numParticles):
		self.numParticles = numParticles

	def getConvertNbody(self):
		return self.convert_nbody

	def setConvertNbody(self, convert_nbody):
		self.convert_nbody = convert_nbody

	def enableDoScale(self):
		self.do_scale = True

	def disableDoScale(self):
		self.do_scale = False

	def getBeta(self):
		return self.beta

	def setBeta(self, beta):
		self.beta = beta

	def getSeed(self):
		return self.seed

	def setSeed(self, seed):
		self.seed = seed

	def enableVerbose(self):
		self.verbose = True

	def disableVerbose(self):
		self.verbose = False

