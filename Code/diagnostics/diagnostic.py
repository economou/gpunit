#!/usr/bin/python
#
# diagnostic.py
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

    def __init__(self, name = "BaseDiagnostic"):
        QListWidgetItem.__init__(self)

        self.conditions = []
        self.setName(name)

    def __reduce__(self):
        """__reduce__ should return a tuple containing the class object, a list
        of arguments to pass to the object upon construction, and a dictionary
        to use as the reconstructed class's member dictionary.

        The dictionary returned should be self.__dict__ unless your diagnostic
        requires GUI elements such as windows. In that case you must copy the
        dict and remove (del) any references to GUI objects.

        Example:
            newDict = self.__dict__
            del newDict["guiwindowname"]

            return (OpenGLDiagnostic, (self.name, self.parent), newDict)"""
        return (self.__class__, (self.name,), {"name":self.name, "conditions":self.conditions})

    def update(self, time, modules):
        """Updates the status of the diagnostic based on the current timestep
        and particle state."""

        raise NotImplementedError("You must implement update in any custom diagnostic in order for it to be updated.")

    def shouldUpdate(self, time, modules) :
        '''Returns a boolean indicating whether this diagnostic should
        be updated given the current experiment state.'''

        bUpdate = True
        for condition in self.conditions :
            bUpdate = bUpdate and condition.shouldUpdate(time, modules)
        return bUpdate

    def setName(self, name):
        """Sets the name and text for display in GUI lists."""
        self.name = name
        self.setText(name)

    def needsGUI(self):
        return False

    def setupGUI(self, parent):
        if self.needsGUI():
            raise NotImplementedError("Diagnostics that require the GUI must implement setupGUI().")
        else:
            pass

    def redraw(self):
        if self.needsGUI():
            raise NotImplementedError("Diagnostics that require the GUI must implement redraw().")
        else:
            pass

    def needsFile(self):
        return False

    def setupFile(self, filename):
        if self.needsGUI():
            raise NotImplementedError("Diagnostics that require file output must implement setupFile().")
        else:
            pass

    def cleanup(self):
        pass
