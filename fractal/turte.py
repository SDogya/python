import cairo
import numpy as np

L = 4
M_I = 6  # колво итераций

WIDTH, HEIGHT = 360, 720
C = 200  # скорсоть изменения угла отклонения
DA = np.pi / 7  # угол отклонения

surface = cairo.SVGSurface("example.svg", WIDTH, HEIGHT)
context = cairo.Context(surface)

context.set_source_rgba(1, 0.2, 0.2, 1)


def forward(i, x, y, a, I):
    context.move_to(x, y)
    context.set_line_width(1 / I)
    nx = x + L / I * np.cos(a)
    ny = y + L / I * np.sin(a)

    context.line_to(nx, ny)

    if i < M_I:

        return forward(i + 1, nx, ny, a, I) + forward(i + 1, nx, ny, a, I)

    b = [nx, ny]
    return b


def func_x(i, x, y, a):
    if i < M_I:
        b = forward(i + 1, x, y, a, i + 1)
        context.move_to(x, y)
        nx = b[0]
        ny = b[1]
        func_x(i + 1, nx, ny, a + DA + np.pi / (C * (i + 1)))
        func_x(i + 1, nx, ny, a - DA - np.pi / (C * (i + 1)))
        b = forward(i + 1, nx, ny, a, i + 1)
        nx = b[0]
        ny = b[1]
        func_x(i + 1, nx, ny, a)


func_x(0, 180, 360, -np.pi / 2)
context.stroke()
surface.write_to_png("example.svg")
