
#!/usr/bin/python
#
# Logger.py
# Rajkumar Jayachandran
#
# Team GPUnit - Senior Design 2011

class Logger:
    def __init__(self, name = "LoggerBase"):
        self.name = name
        self.outputmode = []

    def name():
        '''Gets the name of the logger.'''
        return self.name

    def selectoutput(self,outputmode) :
        '''select output mode for logger '''
        self.outputmode.extend(outputmode)

    def needsGUI(self):
        return False

    def setupGUI(self, parent):
        if self.needsGUI():
            raise NotImplementedError("Logger that require the GUI must implement setupGUI().")
        else:
            pass

    def needsFile(self):
        return False

    def setupFile(self, filename):
        if self.needsGUI():
            raise NotImplementedError("Logger that require file output must implement setupFile().")
        else:
            pass

    def logdata(self,particle) :
        '''gets data from experiment for logger'''
        self.particles.append(particle)

    def toXml() :
        '''Get a xml string representation.'''
        # TODO: implement
        return ""

# Add FileLogger, ConsoleLogger
# Console logging: uses print
# File logging: outputFile = open(filename, 'w')
# outputFile.write(data string)
