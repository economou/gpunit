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

au = 1.495978707e11
ausPerParsec = 206264.8062

def main():
    initGL(900,900)
    done = False

    file = open("pos.txt", 'r')

    stepsTaken = 0
    while True:
        stepsTaken += 1

        line = file.readline()
        if line == "":
            break

        if stepsTaken%1 != 0:
            continue

        pts = line.split(",")
        p0 = [float(f) / au for f in pts[0].split()]
        p1 = [float(f) / au for f in pts[1].split()]

        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor3f(0,1,0)
        glVertex3f(0,1,0)
        glVertex3f(0,-1,0)

        glColor3f(1,0,0)
        glVertex3f(1,0,0)
        glVertex3f(-1,0,0)

        glBegin(GL_POINTS)
        glColor3f(1,0,0)
        glVertex3f(p0[0], p0[1], p0[2])

        glColor3f(0,1,0)
        glVertex3f(p1[0], p1[1], p1[2])
        glEnd()

        pygame.display.flip()

    file.close()
    sleep(10000)

if __name__ == '__main__':
    main()
