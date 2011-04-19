from time import sleep

from OpenGL.GL import *
from OpenGL.GLU import *

from PyQt4.QtOpenGL import QGL, QGLFormat, QGLWidget
from PyQt4.QtCore import QSize

from amuse.support.data.core import Particle, Particles

from Diagnostic import Diagnostic

from PyQt4.QtCore import QCoreApplication

class OpenGLDiagnostic(Diagnostic):
    def __init__(self, name = "OpenGLDiagnostic", dim = (512, 512)):
        Diagnostic.__init__(self, name)

        self.width, self.height = dim
        self.window = GLDiagnosticWindow(self.width, self.height)

    def __reduce__(self):
        newDict = self.__dict__.copy()
        del newDict["window"]

        return (OpenGLDiagnostic, (self.name, ), newDict)

    def setSize(self, dim):
        self.width, self.height = dim
        self.window.setSize(dim)

    def update(self, time, particles):
        self.window.particles = particles

        if not self.window.isVisible():
            self.window.show()

        self.window.update()
        self.window.paintGL()

        # TODO: THIS IS REALLY BAD.
        QCoreApplication.processEvents()
        return True

    def shouldUpdate(self, time, particles):
        return True

class GLDiagnosticWindow(QGLWidget):
    def __init__(self, width, height, parent = None):
        QGLWidget.__init__(self, QGLFormat(QGL.DepthBuffer | QGL.DoubleBuffer), parent)

        self.width_ = width
        self.height_ = height

        self.particles = Particles(0)

    def initializeGL(self):
        glClearColor(0,0,0,1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPointSize(2.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #glOrtho(-2, 2, -2, 2, -2, 2)
        gluPerspective(45.0, 1.0, 0.5, 200);
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(5, 5, 5,
                0, 0, 0,
                0, 0, 1);

    def setSize(self, dim):
        self.width_, self.height_ = dim
        self.resizeGL(self.width_, self.height_)

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

        # Draw the points.
        # TOOD: THIS IS SLOW! Use A VBO or vertex array.
        glColor3f(1,1,1)

        glBegin(GL_POINTS)
        for particle in self.particles:
            pos = particle.position.number
            glVertex3f(pos[0], pos[1], pos[2])
        glEnd()
