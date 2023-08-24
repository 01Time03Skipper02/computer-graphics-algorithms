import math

import glfw
from OpenGL.GL import *

rotate_x = 0.0
rotate_y = 0.0


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "Lab2", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


def cube():
    # front
    glBegin(GL_POLYGON)
    glColor3f(0, 0, 0)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glEnd()
    # back
    glBegin(GL_POLYGON)
    glColor3f(1.0, 0.0, 0)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glEnd()
    # r
    glBegin(GL_POLYGON)
    glColor3f(0, 1.0, 0.0)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glEnd()
    # l
    glBegin(GL_POLYGON)
    glColor3f(0, 0.0, 1.0)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glEnd()
    # t
    glBegin(GL_POLYGON)
    glColor3f(0.5, 0.5, 0.0)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glEnd()
    # b
    glBegin(GL_POLYGON)
    glColor3f(.5, 0.0, .9)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glEnd()


def display(window):
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(640 - 160, 640 - 160, 160, 160)
    glLoadIdentity()
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glPushMatrix()
    glMultMatrixf([
        1, 0, 0, 0,
        0, math.cos(-(math.pi/6)), (-(math.sin(-(math.pi/6)))), 0,
        0, math.sin(-(math.pi/6)), math.cos(-(math.pi/6)), 0,
        0, 0, 0, 1
    ])
    glMultMatrixf([
        math.cos(-(math.pi/6)), 0, math.sin(-(math.pi/6)), 0,
        0, 1, 0, 0,
        (-(math.sin(-(math.pi/6)))), 0, math.cos(-(math.pi/6)), 0,
        0, 0, 0, 1
    ])
    cube()
    glPopMatrix()
    glPushMatrix()
    glMultMatrixf([
          math.cos(rotate_x), 0, math.sin(rotate_x), 0,
          math.sin(rotate_x) * math.sin(rotate_y), math.cos(rotate_y), -1 * math.cos(rotate_x) * math.sin(rotate_y), 0,
          math.sin(rotate_x) * math.cos(rotate_y), -1 * math.sin(rotate_y), -math.cos(rotate_x) * math.cos(rotate_y), 0,
          0, 0, 0, 1])
    glMultMatrixf([
        1, 0, 0, 0,
        0, math.cos(-(math.pi / 6)), (-(math.sin(-(math.pi / 6)))), 0,
        0, math.sin(-(math.pi / 6)), math.cos(-(math.pi / 6)), 0,
        0, 0, 0, 1
    ])
    glMultMatrixf([
        math.cos(-(math.pi / 6)), 0, math.sin(-(math.pi / 6)), 0,
        0, 1, 0, 0,
        (-(math.sin(-(math.pi / 6)))), 0, math.cos(-(math.pi / 6)), 0,
        0, 0, 0, 1
    ])
    glViewport(640 - 500, 640 - 540, 160 * 2, 160 * 2)
    cube()
    glPopMatrix()
    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global rotate_x, rotate_y
    if action == glfw.PRESS:
        if (key == glfw.KEY_RIGHT):
            rotate_y += 0.1

        if (key == glfw.KEY_LEFT):
            rotate_y -= 0.1

        if (key == glfw.KEY_UP):
            rotate_x += 0.1

        if (key == glfw.KEY_DOWN):
            rotate_x -= 0.1


main()