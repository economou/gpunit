from time import sleep

from OpenGL.GL import *
from OpenGL.GLU import *

from PyQt4.QtOpenGL import QGL, QGLFormat, QGLWidget
from PyQt4.QtCore import QSize, SIGNAL, SLOT

from amuse.support.units.units import *
from amuse.support.data.core import Particle, Particles

from diagnostics.diagnostic import Diagnostic

from PyQt4.QtCore import QCoreApplication

class OpenGLDiagnostic(Diagnostic):
    def __init__(self, name = "OpenGLDiagnostic", width = 512, height = 512):
        Diagnostic.__init__(self, name)

        self.width, self.height = width, height
        self.widget = None
        self.parent = None

    def __reduce__(self):
        newDict = self.__dict__.copy()

        # Remove un-serializable references from the class dictionary.
        # (GUI objects usually).
        del newDict["widget"]
        del newDict["parent"]

        return (OpenGLDiagnostic, (self.name, ), newDict)

    def update(self, time, modules):
        if self.parent is None or self.widget is None:
            return True

        self.widget.particles = modules[0].particles
        self.parent.diagnosticUpdated.emit()

        sleep(15.0/1000.0)

        return True

    def redraw(self):
        if not self.widget.isVisible():
            self.widget.show()

        self.widget.update()

    def needsGUI(self):
        return True

    def setupGUI(self, parent):
        self.parent = parent

        if self.widget is None:
            self.widget = GLDiagnosticWidget(self.width, self.height)

    def cleanup(self):
        self.particles = None
        if self.widget is not None:
            self.widget.close()

class GLDiagnosticWidget(QGLWidget):
    def __init__(self, width, height, distanceUnits = AU, parent = None):
        QGLWidget.__init__(self, QGLFormat(QGL.DepthBuffer | QGL.DoubleBuffer), parent)

        self.width_ = width
        self.height_ = height
        self.distanceUnits = distanceUnits

        self.particles = Particles(0)

    def initializeGL(self):
        glClearColor(0,0,0,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPointSize(2.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, 1.0, 0.5, 200);
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(5, 5, 5,
                0, 0, 0,
                0, 0, 1);

    def resizeGL(self, width, height):
        self.resize(self.width_, self.height_)

    def maximumSizeHint(self):
        return QSize(self.width_, self.height_);

    def minimumSizeHint(self):
        return QSize(self.width_, self.height_);

    def sizeHint(self):
        return QSize(self.width_, self.height_);

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw some axes.
        glBegin(GL_LINES)
        glColor3f(1,0,0)
        glVertex3f(0,0,0)
        glVertex3f(1,0,0)

        glColor3f(0,1,0)
        glVertex3f(0,0,0)
        glVertex3f(0,1,0)

        glColor3f(0,0,1)
        glVertex3f(0,0,0)
        glVertex3f(0,0,1)
        glEnd()

        if self.particles is None:
            return

        # Draw the points.
        # TOOD: THIS IS SLOW! Use A VBO or vertex array.
        glColor3f(1,1,1)

        # TODO: investigate this?
        if not isinstance(self.particles, Particles) or len(self.particles) < 1:
            return

        glBegin(GL_POINTS)
        for particle in self.particles:
            pos = particle.position.value_in(self.distanceUnits)
            glVertex3f(pos[0], pos[1], pos[2])
        glEnd()
