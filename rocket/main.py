import json
import random
import matplotlib.pyplot as mpl
import numpy as np
import arcade as a
from typing import (Iterator,List)
from pyglet.math import Vec2

SCREEN_WIDTH = 1280

SCREEN_HEIGHT = 720

SCREEN_TITLE = None

dt = 1 / 5

ITTER_CONST = 6.67 * 10 ** -11

cm_T = []

MP = 10

text = ["ОПИСАНИЕ КНОПОК НА КОТОРЫЕ МОЖНО И НУЖНО ТЫКАТЬ",
        "W - ускорить симуляцию  S - замедлить ",
        "Стрелочками можно двигать камеру , R - вернуть ее в положение центра",
        "+ , - на нумпаде приближает и отдаляет камеру (отдалите)",
        "TAB  -  переключится между объектами",
        "SPACE - поставить паузу (сейчас на паузе) "

        ]


class Anima(a.Sprite):

    def __init__(self, name, mass, center_x: float = 0, center_y: float = 0,
                 hit_box_algorithm: str = "Simple",
                 angle: float = 0, iterration=1,
                 vx=0, vy=0):

        self.iterration = iterration

        self.v = []

        self.t = 0

        self.mass = mass

        self.filename = name

        a.Sprite.__init__(self, center_x=center_x,
                          center_y=center_y,
                          hit_box_algorithm=hit_box_algorithm,
                          angle=angle)

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

        if self.texture_num % 10 == 0:
            self.trajectory.append([self.center_x, self.center_y])

        self.t += dt

        self.v.append([self.change_x, self.change_y, self.t])

    def draw_trajectory(self):
        a.draw_line_strip(self.trajectory, (self.rgb[0], self.rgb[1], self.rgb[2]))

    def load(self, name, sp_x, sp_y, s_x, s_y):

        '''''
        Функция загуржает и обрабатывает лист спрайтов в массив чтобы была анимация 
        '''''

        tlist = []

        for y in range(int(s_y / sp_y)):

            for x in range(int(s_x / sp_x)):
                one_spr = a.load_texture(name, sp_x * x, sp_y * y, sp_x, sp_y)

                tlist.append(one_spr)

        return tlist


class Rokcet(Anima):
    def __init__(self, mass, oil_mass, x, y, vx, vy, name, waste, ux, uy):

        Anima.__init__(self, name, mass + oil_mass, x, y, vx=vx, vy=vy)
        self.oil_mass = oil_mass

        self.waste = waste

        self.u = [ux, uy]
        
 

    def update(self):
        if self.oil_mass > 0:

            if self.oil_mass - self.waste * dt > 0:

                self.change_x += self.u[0] * dt * self.waste / self.mass
                self.change_y += self.u[1] * dt * self.waste / self.mass
                self.mass -= self.waste * dt
                self.oil_mass -= self.waste * dt

            else:
                self.change_x += self.u[0] * self.oil_mass / self.mass
                self.change_y += self.u[1] * self.oil_mass / self.mass
                self.mass -= self.oil_mass
                self.oil_mass = 0

        Anima.update(self)


class ClosedSystem:
    def __init__(self):

        self.list: List[Anima] = []

        self.dr_cm = False
    def __setitem__(self, key, value):
        self.list[key] = value

    def __getitem__(self, key):
        return self.list[key]
    def __iter__(self) -> Iterator[Anima]:

        return iter(self.list)

    def mass_cent(self):
        '''''
            считает и рисует положение центра масс ситсемы
        '''''
        m = 0

        mr = [0, 0]

        for i in self.list:
            m += i.mass

            mr[0] += i.mass * i.center_x

            mr[1] += i.mass * i.center_y

        a.draw_circle_filled(mr[0] / m, mr[1] / m, 10, a.color.RED)

        cm_T.append([mr[0] / m, mr[1] / m])

    def append(self, x: Anima):
        self.list.append(x)

    def draw(self):

        for i in self.list:
            i.draw_trajectory()

        for i in self.list:
            i.draw()

        if self.dr_cm:
            self.mass_cent()
    def __len__(self) -> int:

        return len(self.list)
    

    def interaction(self):

        for main in self.list:

            if main.iterration == 1:

                for sec in self.list:

                    if main != sec:
                        D_X = -(main.center_x - sec.center_x)

                        D_Y = -(main.center_y - sec.center_y)

                        dist = D_X ** 2 + D_Y ** 2

                        main.change_x += ITTER_CONST * sec.mass / (dist ** (3 / 2)) * D_X * dt

                        main.change_y += ITTER_CONST * sec.mass / (dist ** (3 / 2)) * D_Y * dt

    def update(self):
        self.interaction()

        for i in self.list:
            i.update()


class MyGame(a.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
                         vsync=True, center_window=True, update_rate=1 / 64)

        self.set_mouse_visible(True)

        self.camera_sprites = a.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        a.enable_timings()

        self.tek = 0

        self.smesh = [0, 0]

        self.cam_lock = 0

        self.PAUSE = 1
        self.start =0

        self.SPEED = 1

        self.system = ClosedSystem()

    def setup(self):
        v = 2000

        alpha = 30

        self.system.dr_cm = 1

        self.system.append(
            Rokcet(1, 120, 0, 0, 0, 0, "rocket", 3, v * np.cos(np.radians(alpha)), v * np.sin(np.radians(alpha))))

        self.system.append(Anima("earth", 6 * 10 ** 24, 0, -6400000, ))


        self.system[1].scale = 128000


    def on_draw(self):
        a.start_render()

        self.camera_sprites.use()

        self.system.draw()

        if self.start == 0:
            for i in range(text.__len__()):
                a.draw_text(f"{text[i]} ", self.system[self.tek].center_x - self.width / 2+700,
                            self.system[self.tek].center_y  + self.height / 2 - 100 * (i + 1)+300,
                            a.color.WHITE)

    def on_key_press(self, key, modifiers):
        if key == a.key.UP:
            self.smesh[1] += 100

        if key == a.key.DOWN:
            self.smesh[1] -= 100

        if key == a.key.RIGHT:
            self.smesh[0] += 100

        if key == a.key.LEFT:
            self.smesh[0] -= 100

        if key == a.key.R:
            self.smesh = [0, 0]

        if key == a.key.NUM_ADD:
            self.camera_sprites.scale /= 2

        if key == a.key.NUM_SUBTRACT:
            self.camera_sprites.scale *= 2

        if key == a.key.SPACE:
            if self.PAUSE == 1:
                self.PAUSE = 0
                self.start=1

            else:
                self.PAUSE = 1

        if key == a.key.TAB:
            if self.tek + 1 > self.system.__len__() - 1:
                self.tek = 0

            else:
                self.tek += 1

        if key == a.key.W:
            self.SPEED += 1 * MP

        if key == a.key.S and self.SPEED > 1:
            self.SPEED -= 1 * MP

  

    def on_key_release(self, key, modifiers):
        pass


    def on_update(self, delta_time):
        if self.PAUSE == 0:

            for x in range(self.SPEED):

                self.system.update()

                if self.cam_lock == 0:
                    self.scroll_to_player()

   

    def scroll_to_player(self):

        position = Vec2(self.system[self.tek].center_x + self.smesh[0] - self.width / 2,
                        self.system[self.tek].center_y + self.smesh[1] - self.height / 2)

        self.camera_sprites.move_to(position, 1)
        # упоротый движок принимает у всех спрайтов отдельно х и у но у камеры неееет давай херач вектор





window = MyGame()
window.setup()
a.run()

t = []
vx = []
vy = []
for i in window.system.list[0].v:
    t.append(i[2])
    vx.append(i[0])
    vy.append(i[1])

mpl.plot(t, vx)
mpl.plot(t, vy)
mpl.show()
