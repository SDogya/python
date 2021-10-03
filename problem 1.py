import numpy as np #подключаем нампай
import matplotlib.pyplot as plt #подключаем матплот

# Эта программа рисует график функции, заданной выражением ниже

if __name__=='__main__': # функция будет выполнятся только если она "главный процесс"

    plt.ion()       # включает "интерактивность" - без этого дальше почти все бесполезно
    A=0     # величина отклоения
    B=2*np.pi/100       # скорость изменения А
    fig, axes = plt.subplots(1)     # создаем фигуру и одно окошко осей

    fig.set_facecolor('#3C403D')        #у фигуры задаем цвет задника
    axes.set_facecolor('#3C403D')       #у осей задаем цвет задника

    plt.show()      #показываем  окошко

    axes.spines['left'].set_color('#3C403D')# ставим цвет левой оси
    axes.spines['bottom'].set_color('#3C403D')#ставим цвет нижней оси
    axes.spines['top'].set_color('#3C403D')#ставим цвет верхней оси
    axes.spines['right'].set_color('#3C403D')#ставим цвет правой оси
    axes.tick_params(axis='x', colors='#3C403D')# ставим цвет отметок и цифр у х
    axes.tick_params(axis='y', colors='#3C403D')#ставим цвет отметок и цифр у у
    axes.set_aspect(1)# ставим соотношение осей 1 к 1
    radius = 1# задаем радиус - в данной программе бесполезно

    circle = np.linspace(0, 2 * np.pi, 100)  #задаем углы для круга
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)# меняем настройки у окошка
    while ( plt.fignum_exists(1)):  # условие чтобы при закрытии окна программа тоже прекращада работать



        angle = np.linspace(np.pi/2 - A, 2.5 * np.pi -A, 6) # угла для фигуры

        penta_x = radius * np.cos(angle) # коорджинаты х фигуры
        penta_y = radius * np.sin(angle) # коорджинаты у фигуры

        x = radius * np.cos(circle) # координаты круга х
        y = radius * np.sin(circle) #координаты круга у

        bx=[0,0,0,0,0,0] #создаем пусто массив 6 элемнетов

        bx[0] = penta_x[0] #если этого не сделать то будет пятиугольник
        bx[1] = penta_x[2] #
        bx[2] = penta_x[4] #
        bx[3] = penta_x[1] #
        bx[4] = penta_x[3] #
        bx[5] = penta_x[0] #
        penta_x = bx #

        by = [0,0,0,0,0,0] #если этого не сделать то будет пятиугольник
        by[0] = penta_y[0] #
        by[1] = penta_y[2] #
        by[2] = penta_y[4] #
        by[3] = penta_y[1] #
        by[4] = penta_y[3] #
        by[5] = penta_y[0] #
        penta_y= by #

        axes.plot(x, y, color='crimson', linewidth = 5)# рисуем круг с заданой шириной и цветом линии


        axes.plot(penta_x, penta_y, color='crimson', linewidth=4.2)# рисуем фигуру с заданой шириной и цветом линии


        plt.pause(0.000000001)#задержка перед перерисовкой
        axes.clear()# "очистка холста"

        A+=B#изменяем нач позицию фигуры

