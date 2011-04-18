from time import sleep

from OpenGL.GL import *
from OpenGL.GLU import *

from PyQt4.QtOpenGL import QGL, QGLFormat, QGLWidget
from PyQt4.QtCore import QSize

from amuse.support.data.core import Particle, Particles

from Diagnostic import Diagnostic

from PyQt4.QtCore import QCoreApplication

class OpenGLDiagnostic(Diagnostic):
    def __init__(self, name = "OpenGLDiagnostic", parent = None):
        Diagnostic.__init__(self, name)
        self.window = GLDiagnosticWindow()

    def needsGUI(self):
        return True

    def setGUI(self, parent):
        self.window.setParent(parent)

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
    def __init__(self, parent = None):
        QGLWidget.__init__(self, QGLFormat(QGL.DepthBuffer | QGL.DoubleBuffer), parent)
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

    def resizeGL(self, width, height):
        self.resize(512, 512)

    def maximumSizeHint(self):
        return QSize(512, 512);

    def minimumSizeHint(self):
        return QSize(512, 512);

    def sizeHint(self):
        return QSize(512, 512);

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
