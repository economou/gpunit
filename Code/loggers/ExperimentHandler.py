#!/usr/bin/python
#
# ExperimentHandler.py
# Rajkumar Jayachandran
#
# Team GPUnit - Senior Design 2011

class ExperimentHandler :
	
def __init__(self) :
       self.name = " ExperimentHandler baseclass "
       self.loggers = []

def addLogger(logger) :
		'''Adds a logger'''
		self.loggers.append(logger)
def removeLogger(logger) :
		'''Removes a logger'''
		self.loggers.remove(logger)
def getloggers(self) :
           '''returns logger received from logger class'''
           return self.particles
