import math
from OpenGL.GL import *
from shapely.geometry import LineString, Point
import glfw

width, height = 300, 300
history = []
history1 = []
history2 = []
enter_pressed = False
done_second = False
done_first = False
space_pressed = False


class point:
    is_in = None
    merced = False

    def __init__(self, x, y):
        self.x = x
        self.y = y


def line_intersection(a, b, c, d):
    line1 = LineString([a, b])
    line2 = LineString([c, d])

    int_pt = line1.intersection(line2)
    if isinstance(int_pt, LineString):
        return None
    else:
        return [int_pt.x, int_pt.y]


def get_all_intersections(fig_vertexes, slider_vertexes, not_do=False):
    res_in = []
    res_out = []
    res = []
    is_in = True
    for i in range(len(fig_vertexes)):
        intersections = []
        for j in range(len(slider_vertexes)):
            if i != len(fig_vertexes) - 1:
                if j != len(slider_vertexes) - 1:
                    intersection = line_intersection(fig_vertexes[i], fig_vertexes[i + 1], slider_vertexes[j],
                                                     slider_vertexes[j + 1])
                else:
                    intersection = line_intersection(fig_vertexes[i], fig_vertexes[i + 1], slider_vertexes[j],
                                                     slider_vertexes[0])
            else:
                if j != len(slider_vertexes) - 1:
                    intersection = line_intersection(fig_vertexes[i], fig_vertexes[0], slider_vertexes[j],
                                                     slider_vertexes[j + 1])
                else:
                    intersection = line_intersection(fig_vertexes[i], fig_vertexes[0], slider_vertexes[j],
                                                     slider_vertexes[0])
            if intersection is not None:
                intersections.append(intersection)
        intersections.sort(key=lambda intersect: math.sqrt((intersect[0] - fig_vertexes[i][0]) ** 2 +
                                                           (intersect[1] - fig_vertexes[i][1]) ** 2))
        res.append(point(fig_vertexes[i][0], fig_vertexes[i][1]))
        for inter in intersections:
            p = point(inter[0], inter[1])
            res.append(p)
            p.is_in = is_in
            if is_in:
                res_in.append(p)
            else:
                res_out.append(p)
            is_in = not is_in
    return res, res_in, res_out


def generate_sec_points(fig_vertexes, slider_vertexes):
    new_fig_vertexes, ins, outs = get_all_intersections(fig_vertexes, slider_vertexes)
    new_slider_vertexes, _, _ = get_all_intersections(slider_vertexes, fig_vertexes, not_do=True)
    return new_fig_vertexes, new_slider_vertexes, ins, outs


def has_not_merced(a):
    for i in a:
        if not i.merced:
            return True
    return False


def find(a, b):
    k = 0
    for i in a:
        if i.x == b.x and i.y == b.y:
            return k
        k += 1
    return -1


def weiler_atherton(fig_vertexes, slider_vertexes):
    res = []
    new_fig_vertexes, new_slider_vertexes, ins, outs = generate_sec_points(fig_vertexes, slider_vertexes)
    i = 0
    while has_not_merced(outs):
        if not outs[i].merced:
            outs[i].merced = True
            res.append([outs[i].x, outs[i].y])
        j = find(new_fig_vertexes, outs[i])
        while find(ins, new_fig_vertexes[j]) == -1:
            res.append([new_fig_vertexes[j].x, new_fig_vertexes[j].y])
            j += 1
            if j >= len(new_fig_vertexes):
                j = 0

        k = find(new_slider_vertexes, new_fig_vertexes[j])
        while find(outs, new_slider_vertexes[k]) == -1:
            res.append([new_slider_vertexes[k].x, new_slider_vertexes[k].y])
            k += 1
            if k >= len(new_slider_vertexes):
                k = 0
        i += 1
        if i >= len(outs):
            i = 0
    return res


def display(window):
    glViewport(0, 0, width, height)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, height, 0.0, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()
    if not space_pressed:
        if done_first:
            glBegin(GL_LINE_LOOP)
            for i in range(len(history)):
                glVertex2fv([history[i][0], history[i][1]])
            glEnd()
        if done_second:
            glBegin(GL_LINE_LOOP)
            for i in range(len(history1)):
                glVertex2fv([history1[i][0], history1[i][1]])
            glEnd()
    else:
        glBegin(GL_LINE_LOOP)
        for i in range(len(history2)):
            glVertex2fv([history2[i][0], history2[i][1]])
        glEnd()
    glPopMatrix()
    glfw.swap_buffers(window)
    glfw.poll_events()


def mouse_button_callback(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            cur_x, cur_y = glfw.get_cursor_pos(window)
            if not enter_pressed:
                history.append((cur_x, cur_y))
            elif not done_second:
                history1.append((cur_x, cur_y))


def key_callback(window, key, scancode, action, mods):
    global enter_pressed, history, done_first, done_second, history1, space_pressed, history2
    if key == glfw.KEY_ENTER and action == glfw.PRESS:
        if not enter_pressed:
            enter_pressed = True
            done_first = True
        else:
            done_second = True
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        if not space_pressed:
            history2 = weiler_atherton(history, history1)
            space_pressed = True
        else:
            space_pressed = False


def main():
    if not glfw.init():
        return
    window = glfw.create_window(width, height, 'lab5', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_key_callback(window, key_callback)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glDisable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


main()
