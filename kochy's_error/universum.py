import json
import random
from typing import (Iterator, List)

import arcade as a
import numpy as np
from pyglet.math import Vec2

SCREEN_WIDTH = 1920

SCREEN_HEIGHT = 1080

SCREEN_TITLE = None

# Почему тут нет абстрактных классов ? ну я не нашел как их прикрутить чтоб еще сильнее не портить код
ANOTHER_CONSTANT = 2 ** 6
EL = 4
dt = 10 ** EL  # шаг меняя его точность программы  падает хотя даже 100000 еще почти нормально идет

ITTER_CONST = [6.67 * 10 ** -22, 6.67 * 10 ** -11]  # гравитационые постоянные

TICK = ANOTHER_CONSTANT / 2 ** EL  # на какой шаг будет записываться координаты в траекторию.  если поставить большое число получится\
# очень плохая траектория

CM_TICK = ANOTHER_CONSTANT / 2 ** EL  # на какой добавляется точка в  траекторию центра масс

TICK_LIMIT = 300  # на сколько долго будеет отображатсья траектоия . \
# если поставить очень большое число программа будет работать в 6 кадров

SHAPE_TICK = 5 * 2 ** EL  # вот по этой хрени мы будеем рисовать площадь чем она ниже тем лучше, но если сильно маленькая
#  программа умрет
# на точность расчета площади не влияет

MP = 25  # на сколько сильно ускоряется симуляция (не влияет на точность тк физ расчеты не ускоряются )


# от чего зависит конечная точность сравненния площадей
# 1) от dt  чем меньше тем очевидно лучше
# 2) от площади сектора чем меньше площадь тем лучше
# 3) движение центра мас и всей системы в целом  ! хотя можно сделать так чтоб не двигалось

def postroi_orbitu(x, y, future_position, Mass, sx, sy):
    # эта хрень возвращает скорость которая должна быть чтоб была нормальная красивая орбита
    # вообще она должна работать только в обычной физике т.е. где f ∝ 1/R^2
    # но с помошью господа она каким то чудом  работает и где f ∝ 1/R не так корректно но работает
    def set_speed_for_orbit(current_pos, future_position, Mass):
        # a - большая полуось b - меньшая
        def Afeliuss(a, b, M):
            x = (ITTER_CONST[1] * M * (1 - ((a - b) / (a + b))) / a) ** 0.5
            return x

        def Perigelius(b, a, M):
            x = (ITTER_CONST[1] * M * (1 + ((a - b) / (a + b))) / b) ** 0.5
            return x

        if abs(current_pos) <= abs(future_position):
            return Perigelius(abs(current_pos), abs(future_position), Mass)
        else:
            return Afeliuss(abs(current_pos), abs(future_position), Mass)

    xn = x - sx
    yn = y - sy

    a = np.arctan2(yn, xn)

    r = (xn ** 2 + yn ** 2) ** 0.5

    nv = set_speed_for_orbit(r, future_position, Mass)

    vx, vy = nv * -np.sin(a), nv * np.cos(a)

    return vx, vy


####################################################################################################
class sector():
    def __init__(self, x, y):
        self.r, self.g, self.b = random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)
        self.T = 0
        self.coord = [[x, y]]
        self.Acord = [[x, y]]
        self.another_area = 0

    def append(self, lis: list):
        self.coord.append(lis)
        if self.T == SHAPE_TICK:

            self.Acord.append(lis)
            self.T = 0
        else:
            self.T += 1

    def draw(self):
        a.draw_polygon_filled(self.Acord, [self.r, self.g, self.b])

    def gaus_area(self):
        # https://en.wikipedia.org/wiki/Shoelace_formula
        x_y = np.array(self.coord)
        x_y = x_y.reshape(-1, 2)

        x = x_y[:, 0]
        y = x_y[:, 1]

        S1 = np.sum(x * np.roll(y, -1))
        S2 = np.sum(y * np.roll(x, -1))

        area = .5 * np.absolute(S1 - S2)

        print("Плоащадь по гауссу: ", area, " по другому: ", self.another_area)

    def __setitem__(self, key, value):
        self.coord[key] = value

    def __getitem__(self, key):
        return self.coord[key]

    def __iter__(self):
        return iter(self.coord)

    def __len__(self):
        return self.coord.__len__()


class Shape_list:
    def __init__(self):

        self.shapes: [sector] = []

        self.Tumbler = False

    def append(self, s: sector):
        self.shapes.append(s)

    def __setitem__(self, key, value):
        self.shapes[key] = value

    def __getitem__(self, key):
        return self.shapes[key]

    def __iter__(self):
        return iter(self.shapes)

    def draw(self):
        for i in self.shapes:
            i.draw()

    def start(self, x, y):
        self.shapes.append(sector(x, y))

        self.Tumbler = 1

    def work(self, x, y, are):

        if len(self.shapes) > 1:
            if self.shapes[-1].__len__() != self.shapes[0].__len__():
                self.shapes[-1].append([x, y])
                self.shapes[-1].another_area += are
            else:
                self.stop()
        else:
            self.shapes[-1].append([x, y])
            self.shapes[-1].another_area += are

    def stop(self):
        self.Tumbler = 0
        self.shapes[-1].gaus_area()

    def update(self, x, y, are):
        if self.Tumbler == 1:
            self.work(x, y, are)

    def __len__(self):
        return self.shapes.__len__()

    def clear(self):
        self.shapes.clear()


####################################################################################################
class Anima(a.Sprite):

    def __init__(self, name, mass=0, x: float = 0, y: float = 0,

                 angle: float = 0, iterration=1,
                 vx=0, vy=0, scale=1, orbit=1, radius=10 ** 6):

        self.iterration = iterration
        self.orbit = orbit
        self.orbit_radius = radius
        self.t = 0
        self.tick = 0

        self.mass = mass

        a.Sprite.__init__(self, center_x=x,
                          center_y=y,
                          angle=angle, scale=scale)

        self.change_x = vx

        self.change_y = vy

        self.texture_num = 0

        file = open("sprites/" + name + ".json")

        raw = json.load(file)

        self.textures = self.load("sprites/" + name + ".png",
                                  raw["sp_x"], raw["sp_y"],
                                  raw["s_x"], raw["s_y"])

        self.trajectory = []

        self.rgb = [random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)]

    def update(self):

        self.set_texture(self.texture_num)

        if self.texture_num + 1 > self.textures.__len__() - 1:
            self.texture_num = 0

        else:
            self.texture_num += 1

        self.center_x += self.change_x * dt
        self.center_y += self.change_y * dt

        if self.tick % TICK == 0:
            self.trajectory.append([self.center_x, self.center_y])
            self.tick = 1
            if len(self.trajectory) >= TICK_LIMIT:
                self.trajectory.pop(0)

        self.t += dt
        self.tick += 1

    def draw_trajectory(self):
        a.draw_line_strip(self.trajectory, (self.rgb[0], self.rgb[1], self.rgb[2]))

    def load(self, name, sp_x, sp_y, s_x, s_y, animation=0):

        '''''
        Функция загуржает и обрабатывает лист спрайтов в массив чтобы была анимация 
        '''''

        tlist = []

        if animation == True:
            for y in range(int(s_y / sp_y)):

                for x in range(int(s_x / sp_x)):
                    one_spr = a.load_texture(name, sp_x * x, sp_y * y, sp_x, sp_y)

                    tlist.append(one_spr)
        else:
            tlist.append(a.load_texture(name, sp_x * 1, sp_y * 1, sp_x, sp_y))
        return tlist


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
####################################################################################################

class ClosedSystem:

    def __init__(self):

        self.list: List[Anima] = []
        self.cm_T = []
        self.dr_cm = True
        self.T = 0
        self.star_numer: int

        ####################################################################################################

    def __setitem__(self, key, value):
        self.list[key] = value

    ####################################################################################################
    def __getitem__(self, key):
        return self.list[key]

    ####################################################################################################
    def __iter__(self) -> Iterator[Anima]:

        return iter(self.list)

    ####################################################################################################
    def mass_cent(self):
        '''''
            считает и рисует положение центра масс ситсемы
        '''''
        m = 0

        mr = [0, 0]
        ####################################################################################################
        for i in self.list:
            m += i.mass

            mr[0] += i.mass * i.center_x

            mr[1] += i.mass * i.center_y

        a.draw_circle_filled(mr[0] / m, mr[1] / m, 10 * 10 ** 8, a.color.RED)
        if self.T == CM_TICK:
            self.cm_T.append([mr[0] / m, mr[1] / m])
            self.T = 0
        else:
            self.T += 1
        a.draw_line_strip(self.cm_T, (0, 255, 255))

    ####################################################################################################
    def append(self, x: Anima):
        self.list.append(x)

    ####################################################################################################
    def draw(self):

        for i in self.list:
            i.draw_trajectory()

        for i in self.list:
            i.draw()

        if self.dr_cm == True:
            self.mass_cent()

    ####################################################################################################
    def __len__(self) -> int:

        return len(self.list)

    ####################################################################################################
    def interaction(self):  # вот тут происходит физика

        for main in self.list:

            if main.iterration != 0:

                for sec in self.list:

                    if main != sec:
                        K = main.iterration + 1
                        D_X = -(main.center_x - sec.center_x)

                        D_Y = -(main.center_y - sec.center_y)

                        dist = D_X ** 2 + D_Y ** 2

                        main.change_x += ITTER_CONST[K - 2] * sec.mass / (dist ** (K / 2)) * D_X * dt

                        main.change_y += ITTER_CONST[K - 2] * sec.mass / (dist ** (K / 2)) * D_Y * dt

    ####################################################################################################
    def update(self):
        self.interaction()

        for i in self.list:
            i.update()


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
class MyGame(a.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
                         vsync=True, center_window=True, update_rate=1 / 64)

        self.camera_sprites = a.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        a.enable_timings()

        self.tek = 0

        self.choosen = 0

        self.PAUSE = 0

        self.LAW_STEP = 0

        self.SPEED = 1

        self.system = ClosedSystem()

        self.ST = 0

        self.sectors = Shape_list()
        ####################################################################################################

    def setup(self):

        init = json.load(open("systems/clsys3.json"))
        m = 0
        k = 0
        # создаем небесные тела
        for i in init["bodys"]:
            self.system.append(Anima(
                i["name"],
                i["mass"][0] * 10 ** i["mass"][1],
                i["x"][0] * 10 ** i["x"][1], i["y"][0] * 10 ** i["y"][1], i["angle"],
                i["iterration"], i["vx"], i["vy"], 128000000 / 2,
                i["stable orbit"], i["orbit radius"][0] * 10 ** i["orbit radius"][1]
            ))
            # ищем самую массивную хрень и скажем что она тут звезда
            if m < i["mass"][0] * 10 ** i["mass"][1]:
                m = i["mass"][0] * 10 ** i["mass"][1]
                k = len(self.system) - 1
        # cтроим к̶о̶м̶м̶у̶н̶и̶з̶м̶ орбиты
        for i in self.system:
            if i != self.system[k] and i.orbit == 1:
                i.change_x, i.change_y = postroi_orbitu(i.center_x, i.center_y, i.orbit_radius,
                                                        self.system[k].mass,
                                                        self.system[k].center_x, self.system[k].center_y)

        # будем выбранную планету в 4 раза увеличивать
        self.system[self.choosen].scale *= 4

        # вообще системы движутся и звезда как бы должна иметь скрость но чтоб с этим не ...... скажем что все в системе
        # координат звезды
        self.system[k].change_x = 0
        self.system[k].change_y = 0

        self.system.star_numer = k

        self.camera_sprites.scale = 2 * 10 ** 8

    ####################################################################################################
    def on_draw(self):

        a.start_render()

        self.sectors.draw()

        self.camera_sprites.use()

        self.system.draw()

        a.finish_render()

    ####################################################################################################
    def on_key_press(self, key, modifiers):

        if key == a.key.EQUAL:  # =/+ на клавиатуре
            self.camera_sprites.scale /= 2

        if key == a.key.MINUS:
            self.camera_sprites.scale *= 2

        if key == a.key.SPACE:
            self.PAUSE = 1 if self.PAUSE == 0 else 0

        if key == a.key.TAB:
            if self.tek + 1 > self.system.__len__() - 1:
                self.tek = 0
                self.scroll_to_player()

            else:
                self.tek += 1
                self.scroll_to_player()

        if key == a.key.Q and self.LAW_STEP == 0:
            self.sectors.Tumbler = 0
            self.sectors.clear()
            self.system[self.choosen].scale /= 4
            if self.choosen + 1 > self.system.__len__() - 1:
                self.choosen = 0
            else:
                self.choosen += 1

            self.system[self.choosen].scale *= 4

        if key == a.key.W:
            self.SPEED += MP

        if key == a.key.S and self.SPEED > 1:
            self.SPEED -= MP

        if key == a.key.E:
            if self.sectors.__len__() == 1 and self.sectors.Tumbler == 1:
                self.sectors.stop()
            else:
                self.sectors.start(self.system[self.system.star_numer].center_x,
                                   self.system[self.system.star_numer].center_y)

        if key == a.key.R:
            self.sectors.Tumbler = 0
            self.sectors.clear()

    ####################################################################################################
    def on_update(self, delta_time):

        if self.PAUSE == 0:

            for x in range(self.SPEED):
                self.system.update()
                # подсчет площади по простому. он точный на кругах и пот малом dt а вот метод гауса имеют везде примерно
                # одну и ту же точность
                # чтобы убедится что они делают одно и то же можно площадь единичного
                # круга посчитать оба выдадут примерно 3.14...
                x = [self.system[self.choosen].center_x - self.system[self.system.star_numer].center_x,
                     self.system[self.choosen].center_y - self.system[self.system.star_numer].center_y]
                y = [self.system[self.choosen].change_x, self.system[self.choosen].change_y]
                area = dt * 0.5 * np.cross(x, y)

                self.sectors.update(self.system[self.choosen].center_x, self.system[self.choosen].center_y, area)

                self.scroll_to_player()

                ####################################################################################################

    def scroll_to_player(self):
        position = Vec2(self.system[self.tek].center_x - self.width / 2,
                        self.system[self.tek].center_y - self.height / 2)

        self.camera_sprites.move_to(position, 1)
# упоротый движок принимает у всех спрайтов отдельно х и у но у камеры неееет давай херач вектор


####################################################################################################
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#
####################################################################################################


window = MyGame()
window.setup()
a.run()

print("с начала симуляции прошло  ", window.system[0].t / 60 / 60 / 24 / 365,
      " годик/ов/а ")  # сколько времени прошло в реальных годах
# кстати если создать тут землю солнышко и еще ченить тут будут почти реальные периоды оборота
