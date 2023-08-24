import math
import random

import glfw
from OpenGL.GL import *

rotate_x = 0.0
rotate_y = 0.0
posx = 0.0
posy = 0.0
size = 0.0
radius = 0.5
n = 5


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "Lab3", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


def figure():
    vertexesX = []
    vertexesZ = []
    for i in range(n):
        vertexesX.append(radius * math.cos(2 * math.pi * i / n))
        vertexesZ.append(radius * math.sin(2 * math.pi * i / n))
    # front
    for i in range(n):
        glBegin(GL_POLYGON)
        glColor3f(float(random.Random().random()), float(random.Random().random()), float(random.Random().random()))
        glVertex3f(vertexesX[i - 1], -0.5, vertexesZ[i - 1])
        glVertex3f(vertexesX[i - 1], 0.8, vertexesZ[i - 1])
        glVertex3f(vertexesX[i], 0.8, vertexesZ[i])
        glVertex3f(vertexesX[i], -0.5, vertexesZ[i])
        glEnd()

    # up
    glBegin(GL_POLYGON)
    glColor3f(0.5, 0.5, 0.0)
    for i in range(n):
        glVertex3f(vertexesX[i], 0.8, vertexesZ[i])
    glEnd()
    # down
    glBegin(GL_POLYGON)
    glColor3f(0.0, 0.5, 0.5)
    for i in range(n):
        glVertex3f(vertexesX[i], -0.5, vertexesZ[i])
    glEnd()


def display(window):
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(640 - 160, 640 - 160, 160, 160)
    glLoadIdentity()
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glPushMatrix()
    glRotatef(-30, 1, 0, 0)
    glRotatef(-30, 0, 1, 0)

    figure()
    glPopMatrix()
    glPushMatrix()
    glRotatef(-30, 1, 0, 0)
    glRotatef(-30, 0, 1, 0)
    glRotatef(rotate_x, 1, 0, 0)
    glRotatef(rotate_y, 0, 1, 0)

    glViewport(640 - 500, 640 - 540, 160 * 2, 160 * 2)
    figure()
    glPopMatrix()
    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global rotate_x, rotate_y, n
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            rotate_y += 10

        if key == glfw.KEY_LEFT:
            rotate_y -= 10

        if key == glfw.KEY_UP:
            rotate_x += 10

        if key == glfw.KEY_DOWN:
            rotate_x -= 10

        if key == glfw.KEY_W:
            n += 1

        if key == glfw.KEY_S:
            n -= 1

main()