#!/usr/bin/python
#
# Diagnostic.py
#    Abstract Diagnostic class. Objects of subclasses are added to the an
#    Experiment object where it is updated.
#
# 3/1 - Dan Bagnell - created Diagnostic class.
#
# Team GPUnit - Senior Design 2011
#

from PyQt4.QtGui import QListWidgetItem
class Diagnostic(QListWidgetItem):
    '''Abstract Diagnostic class. Objects of subclasses are added to the an
    Experiment object where it is updated.'''

    def __init__(self, name = "DiagnosticBase") :
        self.name = name
        self.conditions = []

        QListWidgetItem.__init__(self)
        self.setText(self.name)

    def __reduce__(self):
        """ Example format for reduce():
        return (ClassName, (member1, member2, ..., memberN), self.__dict__)

        Specific example:
        return (OpenGLDiagnostic, (self.name, self.parent), self.__dict__)"""

        raise NotImplementedError("You must implement __reduce__ in any custom diagnostic in order for it to be serialized.")

    def update(self, time, particles):
        '''This function needs to be overridden by subclasses'''
        # update the diagnostic
        # this method is supposed to be implemented by subclasses
        return False

    def shouldUpdate(self, time, particles) :
        '''Returns a boolean indicating whether this diagnostic should
        be updated given the current experiment state.'''
        bUpdate = True
        for condition in self.conditions :
            bUpdate = bUpdate and condition.shouldUpdate(particles)
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

    def setName(self, name):
        self.name = name
        self.setText(name)
