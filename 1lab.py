from OpenGL.GL import *
import glfw
import math

angle = 0.0
delta = 0.1
posx = 0.0
posy = 0.0
size = 0.0
radius = 0.5
n = 5


def key_callback(window, key, scancode, action, mods):
    global delta
    global angle
    global n
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            n += 1
        if key == 263:  # glfw.KEY_LEFT
            n -= 1


def scroll_callback(window, xoffset, yoffset):
    global size
    if xoffset > 0:
        size -= yoffset / 10
    else:
        size += yoffset / 10


def display(window):
    global angle
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glPushMatrix()
    glRotatef(angle, 0, 0, 1)
    glBegin(GL_POLYGON)
    for i in range(n):
        glColor3f(0.1 + i / 10, 0.1, 0.1)
        posX = radius * math.cos(2 * math.pi * i / n)
        posY = radius * math.sin(2 * math.pi * i / n)
        glVertex2f(posX, posY)
    glEnd()


def main():
    global angle
    if not glfw.init():
        print("glfw trouble")
        return
    window = glfw.create_window(640, 640, "Lab1", None, None)
    if not window:
        glfw.terminate()
        print("window trouble")
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    while not glfw.window_should_close(window):
        display(window)
        glPopMatrix()
        angle += delta
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.destroy_window(window)
    glfw.terminate()


main()
