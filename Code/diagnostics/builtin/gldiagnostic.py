from time import sleep

import math
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

from PyQt4.QtOpenGL import QGL, QGLFormat, QGLWidget
from PyQt4.QtCore import QSize, SIGNAL, SLOT, Qt
from PyQt4.QtGui import QInputDialog

from amuse.support.units.units import *
from amuse.support.data.core import Particle, Particles

from diagnostics.diagnostic import Diagnostic
from exp_design.settings import SettingsDialog

class OpenGLDiagnostic(Diagnostic):
    def __init__(self, name = "OpenGLDiagnostic", width = 512, height = 512, scaleFactor = 1.0):
        Diagnostic.__init__(self, name)

        self.width, self.height = width, height
        self.widget = None
        self.parent = None

        self.scaleFactor = scaleFactor

        self.settings = SettingsDialog(
                inputs = {"Scale Factor:" : "float"},
                defaults = {"Scale Factor:" : self.scaleFactor})

    def __reduce__(self):
        newDict = self.__dict__.copy()

        # Remove un-serializable references from the class dictionary.
        # (GUI objects usually).
        del newDict["widget"]
        del newDict["parent"]
        del newDict["settings"]

        return (OpenGLDiagnostic, (self.name, self.width, self.height, self.scaleFactor), newDict)

    def update(self, time, particles, modules):
        if self.parent is None or self.widget is None:
            return True

        self.widget.particles = particles
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
            self.widget = GLDiagnosticWidget(self.width, self.height, scaleFactor = self.scaleFactor)

    def cleanup(self):
        pass
        #if self.widget is not None:
           #self.widget.setVisible(False)

    def showSettingsDialog(self):
        results = self.settings.getValues()
        if len(results) > 0:
            self.widget.scaleFactor = results["Scale Factor:"]
            self.scaleFactor = results["Scale Factor:"]

class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def inverse(self):
        d = self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z
        return Quaternion(self.w/d, -self.x/d, -self.y/d, -self.z/d)

def qmult(lhs, rhs):
    q = np.array((lhs.x, lhs.y, lhs.z))
    r = np.array((rhs.x, rhs.y, rhs.z))

    w = (lhs.w * rhs.w) - np.dot(q, r)
    v = (r * lhs.w) + (q * rhs.w) + np.cross(q, r)

    return Quaternion(w, v[0], v[1], v[2])

def normalize(v):
    return v / np.linalg.norm(v)

class GLDiagnosticWidget(QGLWidget):
    def __init__(self, width, height, distanceUnits = AU, scaleFactor = 1.0, parent = None):
        QGLWidget.__init__(self, QGLFormat(QGL.DepthBuffer | QGL.DoubleBuffer), parent)

        self.width_ = width
        self.height_ = height
        self.distanceUnits = distanceUnits
        self.scaleFactor = scaleFactor

        self.lastPos = np.array((0.0, 0.0))
        self.viewRotX = 2.0/3.0
        self.viewRotY = 5.5
        self.fovy = 45.0
        self.camPos = np.array((5.0,5.0,5.0))
        self.camLook = np.array((4.0,4.0,4.0))
        self.camForward = -normalize(self.camPos - self.camLook)

        self.particles = Particles(0)

    def initializeGL(self):
        glClearColor(0,0,0,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPointSize(3.0)
        glEnable(GL_POINT_SMOOTH)

        glShadeModel(GL_SMOOTH)

    def resizeGL(self, width, height):
        self.resize(self.width_, self.height_)

    def maximumSizeHint(self):
        return QSize(self.width_, self.height_);

    def minimumSizeHint(self):
        return QSize(self.width_, self.height_);

    def sizeHint(self):
        return QSize(self.width_, self.height_);

    def mousePressEvent(self, event):
        self.lastPos = np.array((event.pos().x(), event.pos().y()))
        QGLWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        dx = float(event.x() - self.lastPos[0])
        dy = float(event.y() - self.lastPos[1])

        if dx != 0 or dy != 0:
            self.viewRotY += np.sin(2.0 * math.pi * (dx / self.width_))
            self.viewRotX += np.sin(2.0 * math.pi * (dy / self.height_))

            if self.viewRotY >= 2.0 * math.pi:
                self.viewRotY = 0.0
            elif self.viewRotY < 0:
                self.viewRotY = 2.0 * math.pi

            if self.viewRotX >= math.pi / 2.0:
                self.viewRotX = math.pi / 2.0 - 1e-5
            elif self.viewRotX <= -math.pi / 2.0:
                self.viewRotX = -math.pi / 2.0 + 1e-5

            self.lastPos = np.array((event.pos().x(), event.pos().y()))
            self.update()

    def keyPressEvent(self, event):
        right = normalize(np.cross(self.camForward, (0.0, 1.0, 0.0)))
        up = normalize(np.cross(right, self.camForward))

        keycode = event.key()

        if keycode == Qt.Key_W:
            self.camPos += self.camForward / 20.0
        elif keycode == Qt.Key_A:
            self.camPos -= right / 20.0
        elif keycode == Qt.Key_S:
            self.camPos -= self.camForward / 20.0
        elif keycode == Qt.Key_D:
            self.camPos += right / 20.0
        elif keycode == Qt.Key_Space:
            self.camPos += up / 20.0
        elif keycode == Qt.Key_Z:
            self.camPos -= up / 20.0
        elif keycode == Qt.Key_Plus or keycode == Qt.Key_Equal:
            self.fovy += 2.0
        elif keycode == Qt.Key_Minus or keycode == Qt.Key_Underscore:
            self.fovy -= 2.0

        self.update()

    def positionCamera(self):
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        gluPerspective(self.fovy, float(self.width_) / self.height_, 0.001, 100)

        q = Quaternion(np.cos(-self.viewRotY/2.0), 0.0, np.sin(-self.viewRotY/2.0), 0.0)
        r = Quaternion(np.cos(-self.viewRotX/2.0), np.sin(-self.viewRotX/2.0), 0.0, 0.0)

        p = Quaternion(0.0, 0.0, 0.0, -1.0)

        pr = qmult(qmult(qmult(q, r), p), qmult(q, r).inverse())
        self.camForward = normalize(np.array((pr.x, pr.y, pr.z)))

        self.camLook = self.camPos + self.camForward

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        gluLookAt(self.camPos[0], self.camPos[1], self.camPos[2],
                self.camLook[0], self.camLook[1], self.camLook[2],
                0.0, 1.0, 0.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.positionCamera()

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

        glMatrixMode(GL_MODELVIEW)
        glBegin(GL_POINTS)
        for particle in self.particles:
            pos = np.array(particle.position.value_in(self.distanceUnits)) * self.scaleFactor
            glVertex3f(pos[0], pos[2], pos[1])
        glEnd()
