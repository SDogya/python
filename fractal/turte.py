import cairo
import numpy as np

L = 4
M_I = 6 # колво итераций

WIDTH, HEIGHT = 360, 720
C =200   # скорсоть изменения угла отклонения
DA = np.pi / 7 # угол отклонения

surface = cairo.SVGSurface("example.svg", WIDTH, HEIGHT)
context = cairo.Context(surface)

context.set_source_rgba(1, 0.2, 0.2, 1)


def F(i, x, y, a, I):
    context.move_to(x, y)
    context.set_line_width(1 / I)
    nx = x + L / I * np.cos(a)
    ny = y + L / I * np.sin(a)

    context.line_to(nx, ny)

    if i < M_I:

        return F(i + 1, nx, ny, a, I) + F(i + 1, nx, ny, a, I)
    else:
        b = [nx, ny]
        return b


def X(i, x, y, a):
    if i < M_I:
        b = F(i + 1, x, y, a, i + 1)
        context.move_to(x, y)
        nx = b[0]
        ny = b[1]
        X(i + 1, nx, ny, a + DA + np.pi / (C * (i + 1)))
        X(i + 1, nx, ny, a - DA - np.pi / (C * (i + 1)))
        b = F(i + 1, nx, ny, a, i + 1)
        nx = b[0]
        ny = b[1]
        X(i + 1, nx, ny, a)


X(0, 180, 360, -np.pi / 2)
context.stroke()
surface.write_to_png("example.svg")
