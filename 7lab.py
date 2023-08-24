import math

import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from math import cos, sin, asin, sqrt, radians
from PIL import Image
import time
import csv

flag_opt = int(input("Оптимизировать? (1 - да, 0 - нет): "))
OPTIMIZATION = True if flag_opt else False

xm, zm = 0, 0.5
light_f = 1
an_f = 0
tx_f = 1
v = [0.01, 0, 0]
verticies = (

    (0.8, 0.6, 0),
    (0.8, 0.8, 0),
    (0.6, 0.8, 0),
    (0.6, 0.6, 0),

    (0.8, 0.6, 0.2),
    (0.8, 0.8, 0.2),
    (0.6, 0.8, 0.2),
    (0.6, 0.6, 0.2),

    (0.8, 0.6, 0),
    (0.8, 0.8, 0),
    (0.8, 0.8, 0.2),
    (0.8, 0.6, 0.2),


    (0.6, 0.8, 0),
    (0.6, 0.6, 0),
    (0.6, 0.6, 0.2),
    (0.6, 0.8, 0.2),


    (0.6, 0.8, 0),
    (0.8, 0.8, 0),
    (0.8, 0.8, 0.2),
    (0.6, 0.8, 0.2),

    (0.6, 0.6, 0),
    (0.8, 0.6, 0),
    (0.8, 0.6, 0.2),
    (0.6, 0.6,  0.2),


)
verticies = list(verticies)

verticies1 = (
    (0.6, 0.0, 0),
    (0.6, 0.6, 0),
    (0.0, 0.6, 0),
    (0.0, 0.0, 0),

    (0.6, 0.0, 0.6),
    (0.6, 0.6, 0.6),
    (0.0, 0.6, 0.6),
    (0.0, 0.0, 0.6),

    (0.6, 0.0, 0),
    (0.6, 0.6, 0),
    (0.6, 0.6, 0.6),
    (0.6, 0.0, 0.6),

    (0.0, 0.6, 0),
    (0.0, 0.0, 0),
    (0.0, 0.0, 0.6),
    (0.0, 0.6, 0.6),

    (0.0, 0.6, 0),
    (0.6, 0.6, 0),
    (0.6, 0.6, 0.6),
    (0.0, 0.6, 0.6),

    (0.0, 0.0, 0),
    (0.6, 0.0, 0),
    (0.6, 0.0, 0.6),
    (0.0, 0.0, 0.6),


)
verticies1 = list(verticies1)

colors = (
    (0, 1, 1),
    (0, 0, 1),
    (0, 1, 0),
    (1, 0, 0),
    (1, 0, 1),
    (1, 1, 0),

)

e = (
    (0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15), (16, 17, 18, 19), (20, 21, 22, 23)
)

f = 0

mode = 0
ang = 0
angx = 0
arcz = 0
modef = 0
textid = -1


def load_tex():
    global textid
    glEnable(GL_TEXTURE_2D)
    textid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textid)
    image = Image.open('7lab_texture.jpeg')
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA,
GL_UNSIGNED_BYTE, img_data)


def count_normal(a, b, c):
    x0, y0, z0 = a
    x1, y1, z1 = b
    x2, y2, z2 = c
    ux, uy, uz = [x1 - x0, y1 - y0, z1 - z0]
    vx, vy, vz = [x2 - x0, y2 - y0, z2 - z0]
    normal = [uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx]
    l = sqrt(normal[0] * normal[0] + normal[1] * normal[1] + normal[2] * normal[2])
    normal[0] /= l
    normal[1] /= l
    normal[2] /= l
    return normal


def light_enable():

    if not OPTIMIZATION:

        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)
        glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    else:
        glShadeModel(GL_FLAT)
        glDisable(GL_NORMALIZE)
    light0_position = [0, 0, 1, 1]
    spot_direction = [0, 0, -1]
    light0_diffuse = [0.4, 0.7, 0.2]

    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 180.0)
    glLightfv(GL_LIGHT0, GL_POSITION, light0_position)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spot_direction)
    glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, 0)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.5)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.05)



def count_conflict(fig, v):
    mx, mn = -2, 2
    for x in fig:
        if max(x[:2]) > mx:
            mx = max(x)
        if min(x[:2]) < mn:
            mn = min(x)
    if mx >= 1 or mn <= -1:
        v[0] = -v[0]
        v[1] = -v[1]
        v[2] = -v[2]
    return v
def animation(fig, v):
    new_fig = []
    for x in fig:
        x = list(x)
        x[0] += v[0]
        x[1] += v[1]
        x[2] += v[2]
        new_fig.append(x)
    v = count_conflict(new_fig, v)
    return new_fig, v


def myRotate(ang, x, y, z):
    c = cos(radians(ang))
    s = sin(radians(ang))
    modd = sqrt(x ** 2 + y ** 2 + z ** 2)
    x /= modd
    y /= modd
    z /= modd

    glMultMatrixd([x * x * (1 - c) + c, y * x * (1 - c) + z * s, x * z * (1 - c) - y * s, 0,
                   x * y * (1 - c) - z * s, y * y * (1 - c) + c, y * z * (1 - c) + x * s, 0,
                   x * z * (1 - c) + y * s, y * z * (1 - c) - x * s, z * z * (1 - c) + c, 0,
                   0, 0, 0, 1])


def draw_figure():
    global verticies1, v, textid
    if an_f:
        verticies1, v = animation(verticies1, v)
    if tx_f:
        glBindTexture(GL_TEXTURE_2D, textid)
    lis = 0
    if OPTIMIZATION:
        lis = glGenLists(1)
    if lis != 0 or not OPTIMIZATION:
        if OPTIMIZATION:
            glNewList(lis, GL_COMPILE)
        for index, i in enumerate(e):
            glBegin(GL_POLYGON)
            normal = count_normal(verticies1[i[0]], verticies1[i[1]], verticies1[i[2]])
            glNormal3f(normal[0], normal[1], normal[2])
            t = [[0, 0], [1, 0], [1, 1], [0, 1]]
            k = 0
            for j in i:
                if tx_f:
                    glTexCoord2f(t[k][0], t[k][1])
                glVertex3fv(verticies1[j])
                k += 1
            glEnd()
        if OPTIMIZATION:
            glEndList()
    return lis

start_time = time.time()
fps = 0
fps_dict = []
counter = 1
def display(window):
    global mode, f, ang, zm, xm, angx, arcz, modf, verticies1, v, fps, start_time,counter,fps_dict
    lis = 0
    if OPTIMIZATION:
        lis = draw_figure()
    while not glfw.window_should_close(window):
        glViewport(-100, -100, 800, 800)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glRotate(5, 1, 1, 0)
        if OPTIMIZATION:
            glCallList(lis)
        else:
            draw_figure()
        fps += 1
        stop_time = time.time()
        if (stop_time - start_time) > 1:
            fps_dict.append({'num': counter, 'fps': int(round(fps/(stop_time - start_time)))})
            counter += 1
            if counter == 10:
                f_name = 'with_optimization' if OPTIMIZATION else 'without_optimization'
                with open(f'{f_name}.csv', 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fps_dict[0].keys())
                    writer.writeheader()
                    writer.writerows(fps_dict)
                    print("done")
            start_time = time.time()
            fps = 0
        glPopMatrix()
        glFlush()
        glfw.swap_buffers(window)
        glfw.poll_events()



def key_callback(window, key, scancode, action, mods):
    global light_f, an_f, tx_f
    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            light_f += 1
            if light_f > 1:
                light_f = 0
            if light_f:
                glEnable(GL_LIGHTING)
                glEnable(GL_LIGHT0)
                light_enable()
            else:
                glDisable(GL_LIGHTING)
                glDisable(GL_LIGHT0)
        if key == glfw.KEY_V:
            an_f += 1
            if an_f > 1:
                an_f = 0
        if key == glfw.KEY_T:
            tx_f += 1
            if tx_f > 1:
                tx_f = 0



def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, 'lab7', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glDisable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    load_tex()

    display(window)
    glfw.destroy_window(window)
    glfw.terminate()


main()