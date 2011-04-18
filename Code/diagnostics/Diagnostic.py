#!/usr/bin/python
#
# Diagnostic.py
#	Abstract Diagnostic class. Objects of subclasses are added to the an
#	Experiment object where it is updated.
#
# 3/1 - Dan Bagnell - created Diagnostic class.
#
# Team GPUnit - Senior Design 2011
#

class Diagnostic :
	'''Abstract Diagnostic class. Objects of subclasses are added to the an
	Experiment object where it is updated.'''

	def __init__(self) :
		self.name = "Abstract Diagnostic base class"
		self.conditions = []

	def update(self, particles) :
		'''This function needs to be overridden by subclasses'''
		# update the diagnostic
		# this method is supposed to be implemented by subclasses
		return False

	def name(self) :
		'''Gets the name of the Diagnostic.'''
		return self.name

	def shouldUpdate(self, time,state) :
		'''Returns a boolean indicating whether this diagnostic should
		be updated given the current experiment state.'''
		bUpdate = True
		for condition in self.conditions :
			bUpdate = bUpdate and condition.shouldUpdate(state)
		return bUpdate

	def addCondition(self, condition) :
		'''Add a condition.'''
		self.conditions.append(condition)

	def addConditions(self, conditions) :
		'''Add a list of conditions.'''
		self.conditions.extend(conditions)

	def removeCondition(self, condition) :
		'''Remove a condition.'''
		self.conditions.remove(condition)
	
	def toXml(self) :
		'''Get a xml string representation.'''
		# TODO: implement
		return ""


