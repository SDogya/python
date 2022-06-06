import os
import numpy as np
import cv2


def callback(x):
    pass


def Obr(fname, blur_size=30, ch="bloob", WINDOW=False):
    X = []
    Y = []
    T = []
    t = 0
    DELAY = 1
    r = (0, 0, 0, 0)
    bbox = (0, 0, 0, 0)
    Video_FILE = os.path.join("Input", fname)
    cap = cv2.VideoCapture(Video_FILE)
    x0, y0 = -1, -1
    n = int(blur_size)
    fps = cap.get(cv2.CAP_PROP_FPS)
    Duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps

    scale_percent = 100
    # оставь надеждуниже опустившийся
    if ch == "bloob":

        k = 1
        R = 1
        pause = -1
        while (1):
            if pause == -1 or o == 1:
                ret, frame = cap.read()

            if ret == True:

                while r == (0, 0, 0, 0):
                    r = cv2.selectROI(frame, False)
                    cv2.destroyAllWindows()
                if pause == -1 or o == 1:
                    o=0
                    rame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
                    # while k==0:
                    #     k = cv2.selectROI(frame, False)
                    #     k= 7.5 /(k[2])
                    #     cv2.destroyAllWindows()
                    #     print(k)
                    # while R == 0:
                    #         R = cv2.selectROI(frame, False)
                    #         R = (R[2])*k
                    #         cv2.destroyAllWindows()
                    #         print(R)
                    hsv = cv2.blur(rame, (n, n))
                    # hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2RGB)
                    hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
                    hsv = cv2.threshold(hsv, 0, 255,
                                        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                    hsv = cv2.bitwise_not(hsv)
                    hsv = cv2.cvtColor(hsv, cv2.COLOR_GRAY2BGR)

                    # resize image
                # width = int(frame.shape[1] * scale_percent / 100)
                # height = int(frame.shape[0] * scale_percent / 100)
                # dim = (width, height)
                # hsv = cv2.resize(hsv, dim, interpolation=cv2.INTER_AREA)

                if WINDOW:

                    merge = cv2.hconcat([rame, hsv])
                    cv2.imshow("Keypoints", merge)
                    x = cv2.waitKey(DELAY) & 0xff
                    if x == 32:
                        pause *= -1
                    if x == ord("o"):
                        o = 1
                    if x == ord("s"):
                        cv2.imwrite("gettedFrame.png", merge)
                        print("fuck")
                    pass
            else:
                break
            t += 1 / fps

        cv2.destroyAllWindows()
        cap.release()


from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw()
name = askopenfilename().split("/")[-1]
Obr(name, WINDOW=1)
