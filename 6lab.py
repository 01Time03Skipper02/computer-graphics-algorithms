import glfw
import numpy as np
from OpenGL.GL import *
import math
from PIL import Image

tetha = 5
phi = 1
size = 0.5
angle = 0.0
angle2 = 0
delta = 1
n = 10
flag = True
texture = 0
speed = 0.002
direction = [0, 1, 0, 5]
delta_x = 0
delta_y = 0
delta_z = 0
border_x = 1
border_y = 1
border_z = 1

im = Image.open('6lab_texture.jpg')
width = im.width
height = im.height


def getnorm(a, b, c):
    mult = 0
    n = [0] * 3
    n[0] = (b[1] - a[1]) * (c[2] - a[2]) - (b[2] - a[2]) * (c[1] - a[1])
    n[1] = (c[0] - a[0]) * (b[2] - a[2]) - (b[0] - a[0]) * (c[2] - a[2])
    n[2] = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
    for i in range(3):
        mult += a[i] * n[i]
    if mult < 0:
        for j in range(3):
            n[j] = -n[j]
    a = [b[0] - a[0], b[1] - a[1], b[2] - a[2]]
    b = [c[0] - a[0], c[1] - a[1], c[2] - a[2]]
    norm = np.cross(a, b)
    return norm


def drawsq():
    global size, delta_x, delta_y, delta_z
    delta_x += speed * direction[0]
    delta_y += speed * direction[1]
    delta_z += speed * direction[2]
    if abs(delta_x) >= border_x:
        direction[0] = -direction[0]
    if abs(delta_y) >= border_y:
        direction[1] = -direction[1]
    if abs(delta_z) >= border_z:
        direction[2] = -direction[2]
    for j in range(1, n):
        i = 0
        glBegin(GL_QUAD_STRIP)
        while i <= 2 * math.pi:
            m = size - j / n * size
            m_pred = size - (j - 1) / n * size
            x = m * math.cos(i) * math.cos(j / n) + delta_x
            x_pred = m_pred * math.cos(i) * math.cos((j - 1) / n) + delta_x
            y = m * math.sin(i) * math.cos(j / n) + delta_y
            y_pred = m_pred * math.sin(i) * math.cos((j - 1) / n) + delta_y
            z = j / n + delta_z
            z_pred = (j - 1) / n + delta_z
            glColor3f(1, 1, 1)
            norm = getnorm([x_pred, y_pred, (j - 1 / n)], [x, y, j / n],
                           [m * math.cos(i + math.pi / 2) * math.cos(j / n),
                            m * math.sin(i + math.pi / 2) * math.cos(j / n), j / n])
            glNormal3d(norm[0], norm[1], norm[2])
            glTexCoord2f(i/(2*math.pi), 1)

            glVertex3f(x, y, z)
            glTexCoord2f(0, i/(2*math.pi))
            glVertex3f(x_pred, y_pred, z_pred)

            i += math.pi / 2
        glEnd()


def display(window):
    glEnable(GL_TEXTURE_2D)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    material_diffuse = [0, 0, 0., 0.]
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material_diffuse)
    glBindTexture(GL_TEXTURE_2D, texture)
    light3_diffuse = [0.4, 0.7, .1]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light3_diffuse)
    light3_position = [0.1, 1.1, .0, 1.0]
    glPointSize(5)
    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 1)

    glTexCoord2f(0, 1)
    glNormal3f(0., 1.1, .0, )

    glVertex3f(.1, 1., .0)
    glNormal3f(0., -1.1, .0, )

    glTexCoord2f(1, 0)
    glVertex3f(0.7, -0.6, 0.)

    glTexCoord2f(0.5, 0.5)
    glVertex3f(-0.7, -0.6, 0.)
    glEnd()

    glLightfv(GL_LIGHT0, GL_POSITION, light3_position)
    glLightfv(GL_LIGHT1, GL_POSITION, [0.7, -1.0, 0., 1.0])
    glLightfv(GL_LIGHT2, GL_POSITION, [-1., -1.0, 0., 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 0, 0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0, 1, 0])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0, 0, 1])
    glEnable(GL_NORMALIZE)
    if flag:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glPushMatrix()
    glRotatef(angle2, 1, 0, 0)
    glRotate(angle, 0, 0, 1)
    glPushMatrix()
    drawsq()
    glPopMatrix()
    glPopMatrix()

    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global angle, angle2, flag
    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            flag = not flag


def scroll_callback(window, xoffset, yoffset):
    global size
    if xoffset > 0:
        size -= yoffset / 10
    else:
        size += yoffset / 10


def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Lab6", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.2, 1.2, -1.2, 1.2, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glGenTextures(1, texture)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, im.tobytes())
    glBindTexture(GL_TEXTURE_2D, 0)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


main()
