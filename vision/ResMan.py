import pandas as pd
import numpy as np
from vispy import plot as vp
import vispy.io as io
import os

from scipy.optimize import curve_fit as cf
from tkinter import Tk
from tkinter.filedialog import askopenfilename

 # we don't want a full GUI, so keep the root window from appearing
Tk().withdraw()
name = askopenfilename().split("/")[-1]
print(name)
# name = f"J4.mp4"

NAMES = ["bloob", "csrt", "kfc"]
CLR = {"bloob": [1, 0, 0], "csrt": [0, 1, 0], "kfc": [0, 0, 1]}
name = os.path.join("Output", "Data", f'{name[:-4]}', f'{name[:-4]}.xlsx')

T, X = [], []
# data import
xl = pd.ExcelFile(name)
coord = "y"

for mname in xl.sheet_names:
    df = pd.read_excel(name, sheet_name=mname)

    me = []

    for i in range(len(df[coord]) - 1):
        me.append(abs(df[coord][i] - df[coord][i + 1]))
    me = np.array(me)
    me = 5 * me.std()
    x = []
    t = []
    for i in range(len(df[coord]) - 1):
        try:
            # if abs(df[coord][i-1]-df[coord][i])<me or abs(df[coord][i+1]-df[coord][i])<me :
            x.append(df[coord][i])
            t.append(df["t"][i])

        except:
            pass




    def f(x,a, l, w, b):

        return max(x) * np.exp(x/10 * -l+a) *np.cos(x * w - b)


    # a, l, w, b = cf(f, t, mes,maxfev = 8000)[0]
    # print(l, w, b)

    plot1 = vp.Fig(size=(2560, 1440), show=False)

    plot1[0, 0].plot((t, x),
                     symbol='o', width=0,
                     edge_color=None,
                     edge_width=0,
                     color=[0, 0, 0],

                     marker_size=4,
                     face_color=[0, 0, 0])

    # mes = f(np.array(t),a,l,w,b)

    plot1[0, 0].plot((t, x),
                     symbol='o', width=1,
                     edge_color=None,
                     edge_width=0,
                     color=[0, 0, 0],

                     marker_size=0,
                     face_color=[0, 0, 0])
    #############################
    # build your visuals
    # Scatter3D = scene.visuals.create_visual_node(visuals.MarkersVisual)
    #
    # # The real-things : plot using scene
    # # build canvas
    # canvas = scene.SceneCanvas(keys='interactive', show=True, bgcolor='w')
    #
    #
    #
    # # Add a ViewBox to let the user zoom/rotate/grid
    # view = canvas.central_widget.add_view()
    #
    # view.camera = 'turntable'
    # view.camera.fov = 45
    # view.camera.distance = 100
    #
    # grid = visual.GridLines()
    # view.camera.translate_speed = 25
    # view.add(grid)
    #
    #
    # # data
    #
    #
    # data = df
    # n = len(data["y"])
    # pos = np.zeros((n, 3))
    # colors = np.ones((n, 4), dtype=np.float32)
    #
    # for i in range(len(data["mes"])):
    #     mes = data["mes"][i]
    #     y = data["y"][i]
    #     z = data["t"][i]
    #     pos[i] = mes, y, z
    #     colors[i] = (abs((mes - df["mes"].min()) / (df["mes"].max() - df["mes"].min())),
    #                  abs((y - df["y"].min()) / (df["y"].max() - df["y"].min())),
    #                  abs((z - df["t"].min()) / (df["t"].max() - df["t"].min()))
    #                  , 1)
    #
    # # plot
    # p1 = Scatter3D(parent=view.scene)
    # p1.set_gl_state('translucent', blend=True, depth_test=True)
    # p1.set_data(pos, face_color=colors)
    #
    # # run
    # app.run()

    T.append(t)
    X.append(x)
    # img = plt.render()
    # io.write_png( f'{name[:-4]}_{mname}.png',img)
    plot1.show(run=True)

    # import cv2
    # img = cv2.imread(f'{name[:-4]}_{mname}.png')
    # img =   cv2.bitwise_not(img)
    # cv2.imwrite(f'{name[:-4]}_{mname}_i.png',img)
    # import matplotlib.pyplot as plt
    # plt.plot(t,mes)
    # plt.savefig(f'{name[:-4]}_{mname}.svg')
# plt = vp.Fig(size=(2560, 1440), show=False)
# for i in [0,1,2]:
#     mes = X[i]
#     t =T[i]
#     plt[0, 0].plot((t, mes),
#                      symbol='o', width=0,
#                      edge_color=None,
#                      edge_width=0,
#                      color=CLR[NAMES[i]],
#                      marker_size=4,
#                      face_color=CLR[NAMES[i]])
# img = plt.render()
# io.write_png(f'{name[:-4]}_superp.png', img)
