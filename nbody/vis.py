#!/usr/bin/python

import pygame
from pygame.locals import *

from time import sleep

from OpenGL.GL import *
from OpenGL.GLU import *

def initGL(w, h):
    pygame.init()
    pygame.display.set_mode((w, h), pygame.OPENGL|pygame.DOUBLEBUF)

    glClearColor(0,0,0,1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-2, 2, -2, 2)
    glMatrixMode(GL_MODELVIEW)

au = 1.495978707e8 / 1e-8

def main():
    initGL(512,512)
    done = False

    p0 = []
    p1 = []
    file = open("pos.txt", 'r')
    for line in file:
        pts = line.split(",")
        p0.insert(0, [float(f) for f in pts[0].split()])
        p1.insert(0, [float(f) for f in pts[1].split()])

    p0 = [x for x in reversed(p0)]
    p1 = [x for x in reversed(p1)]

    for i in range(0, len(p0)):
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor3f(0,1,0)
        glVertex3f(0,1,0)
        glVertex3f(0,-1,0)

        glColor3f(1,0,0)
        glVertex3f(1,0,0)
        glVertex3f(-1,0,0)

        glBegin(GL_POINTS)
        glColor3f(1,0,0)
        glVertex3f(p0[i][0], p0[i][1], p0[i][2])

        glColor3f(0,0,1)
        glVertex3f(p1[i][0], p1[i][1], p1[i][2])
        glEnd()

        pygame.display.flip()

if __name__ == '__main__':
    main()
