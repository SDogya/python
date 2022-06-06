import cv2
import os
import matplotlib.animation as animation
import matplotlib


import matplotlib.pyplot as plt

import numpy as np
import matplotlib.ticker as ticker

# Const and settings :

from tkinter import Tk
from tkinter.filedialog import askopenfilename

# file
Tk().withdraw()
name = askopenfilename(filetypes=[("videos", ".mp4 .AVI .MOV")]).split("/")[-1]

gname = "graph.mp4"
fname = "fcomb.mp4"
outname = "final.mp4"
speed = 0.8/1.5
blur_size = (25,25)
scale_percent = 100

# variables

X, T = [], []
cap = cv2.VideoCapture(os.path.join("Input", name))

# choose frame size

r = cv2.selectROI(cv2.VideoCapture(os.path.join("Input", name)).read()[1], False)
cv2.destroyAllWindows()
cap.release()
#

cap = cv2.VideoCapture(os.path.join("Input", name))
fps = cap.get(cv2.CAP_PROP_FPS)
Duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
print(fps)
# parametres of blob

params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 3000
params.maxArea = 9000

# create detector
detector = cv2.SimpleBlobDetector_create(params)

# create video writer
w = int(r[2] * scale_percent / 100)
h = int(r[3] * scale_percent / 100)
print(w,h)
out = cv2.VideoWriter(fname, cv2.VideoWriter_fourcc(*'mp4v'), speed * fps, (int(2 * w), int(h)))

# create fig and axis for plot
# xplus = max(T) / 100 * 10
# yplus = max(X) / 100 * 10

# axis = plt.axes(ylim=(min(X) - yplus, max(X) + yplus),
#                 xlim=(min(T) - xplus, max(T) + xplus))


# video processing
t = 0
x0 = -1
while True:
    ret, frame = cap.read()
    if ret == True:

        frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]  # cut the frame
        hsv = cv2.blur(frame, blur_size)  # blur
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2RGB)  # BGR to RGB - АХТУНГ ЭТО ВАЖНЫЙ КАСТЫЛЬ БЕЗ КОТОРОГО ВСЕ ИДЕТ НАХУЙ
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)  # convert to gray
        hsv = cv2.threshold(hsv, 0, 255,
                            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]  # radical binary
        hsv = cv2.bitwise_not(hsv)  # inverse color

        # resize

        # width = int(hsv.shape[1] * scale_percent / 100)
        # height = int(hsv.shape[0] * scale_percent / 100)
        # dim = (width, height)
        #
        # hsv = cv2.resize(hsv, dim, interpolation=cv2.INTER_AREA)  # decment this

        # find the bloobs
        try:
            keypoints = detector.detect(hsv)  # get some shit
            x = np.array(cv2.KeyPoint_convert(keypoints)[:, 1]).mean()  # y
            hsv = cv2.drawKeypoints(hsv, keypoints, np.array([]), (0, 0, 255),
                                    cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) # draw circles
            if x0 == -1:
                x0 = x
            T.append(t)
            X.append((x - x0) * 100 / scale_percent)
            # b = cv2.resize(cv2.imread("img.png"), (int(w * 1.5), int(h)), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
            out.write(cv2.hconcat([frame, hsv]))

        except:
            pass
        cv2.imshow("S", hsv)
        if cv2.waitKey(1) == ord("s"):
            break


        # save coord for plot


        t += 1 / fps
    else:
        break

# time : 6:21

xplus = max(T) / 100 * 10
yplus = max(X) / 100 * 10
fig = plt.figure()
axis = plt.axes(ylim=(min(X) - yplus, max(X) + yplus),
                xlim=(min(T) - xplus, max(T) + xplus))

xdata, ydata = [], []
l = len(X)

# axis.scatter(T, X, s=4)

fig.clear()
print(T[0],X[0])

def animate(i):
    print(i + 1, "/", l)
    fig.clear()
    xdata.append(T[i])
    ydata.append(X[i])

    ax = fig.add_subplot(111, ylim=(min(X) - yplus, max(X) + yplus), xlim=(min(T) - xplus, max(T) + xplus))
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.xaxis.set_minor_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_minor_locator(ticker.NullLocator())
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    s = ax.scatter(xdata, ydata, s=4)


anim = animation.FuncAnimation(fig, animate,init_func=None ,frames=len(T), interval=1)
anim.save("graph.mp4", writer="ffmpeg", fps=fps, dpi=200)

cap.release()
out.release()

one = cv2.VideoCapture(fname)
two = cv2.VideoCapture(gname)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = one.get(cv2.CAP_PROP_FPS)
w1 = one.get(cv2.CAP_PROP_FRAME_WIDTH)
h1 = one.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(w1, h1)
w1 = w1 / 2
print(w1, h1)

out = cv2.VideoWriter(outname, fourcc, 50, (int(w1 * 3.5), int(h1)))

while True:
    ret, fr1 = one.read()
    ret, fr2 = two.read()
    if ret == True:
        b = cv2.resize(fr2, (int(w1 * 1.5), int(h1)), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)  # NEAREST or AREA

        out.write(cv2.hconcat([fr1, b]))
    else:
        break

one.release()
two.release()
out.release()
cv2.destroyAllWindows()
