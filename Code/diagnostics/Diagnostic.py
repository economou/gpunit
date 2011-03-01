#!/usr/bin/python
#
# Diagnostic.py
#	Abstract Diagnostic class. Objects of subclasses are added to the an
#	Experiment object where it is updated.
#
# 3/1 - Dan Bagnell - created Diagnostic class
#
# Team GPUnit - Senior Design 2011
#

class Diagnostic :
	'''Abstract Diagnostic class. Objects of subclasses are added to the an
	Experiment object where it is updated.'''

	def __init__(self, name) :
		self.name = name
		self.conditions = []

	def update(particles) :
		# update the diagnostic
		# this method is supposed to be implemented by subclasses
		# inheritance in python?
		return False

	def name() :
		return self.name

	def shouldUpdate(state) :
		bUpdate = True
		for condition in self.conditions :
			bUpdate = bUpdate and condition.shouldUpdate(state)
		return bUpdate

	def addCondition(condition) :
		self.conditions.append(condition)

	def addConditions(conditions) :
		self.conditions.extend(conditions)

	def removeCondition(condition) :
		self.conditions.remove(condition)
	
	def toXml() :
		# TODO: implement
		return ""
