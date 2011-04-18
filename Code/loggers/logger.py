
#!/usr/bin/python
#
# Logger.py
# Rajkumar Jayachandran
#
# Team GPUnit - Senior Design 2011

class Logger :
	
def __init__(self) :
       self.name = " Logger subclass "
       self.outputmode = []
def name() :
		'''Gets the name of the logger.'''
		return self.name


def selectoutput(self,outputmode) :
		'''select output mode for logger '''
		self.outputmode.extend(outputmode)

def logdata(self,particle) :
           '''gets data from experiment for logger'''
           self.particles.append(particle)

def toXml() :
		'''Get a xml string representation.'''
		# TODO: implement
		return ""


























