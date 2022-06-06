import pandas as pd
import os
import numpy as np
import cv2

name = "V15"
fname = name + ".mp4"
Video_FILE = os.path.join("../Input", fname)
WINDOW = 0
DELAY = 10
ALL = 0
SAVE = 1
n = int(1)
MEAN = 0

if not os.path.isfile(os.path.join("../Input", fname)):
    cv2.imshow('img2', cv2.imread(os.path.join("../errors", "error.png")))
    import pygame

    pygame.mixer.init()
    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() / 12)
    pygame.mixer.music.load(os.path.join("../errors", "error.mp3"))
    pygame.mixer.music.play()
    cv2.waitKey(2000)
    raise "Файл не обнаружен"

cap = cv2.VideoCapture(Video_FILE)
# red_lower = np.intc(np.array([165, 0.3 * 255, 0.3 * 255]))
# red_upper = np.intc(np.array([180, 255, 255]))
red_lower = np.intc(np.array([170, 0.5 * 255, 0.5 * 255]))
red_upper = np.intc(np.array([180, 255, 255]))
connectivity = 8

############################################


X = []
Y = []

while (1):
    ret, frame = cap.read()

    if ret == True:
        blur = cv2.blur(frame, (n, n))
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, red_lower, red_upper)
        output = cv2.connectedComponentsWithStats(mask, connectivity, cv2.CV_32S)
        try:
            if MEAN == 1:
                x, y = np.mean((output[3][1:]), axis=0)
            else:
                x, y = output[3][1:][:][0]
            x = int(x)
            y = int(y)

            if SAVE == 1:
                X.append(x)
                Y.append(y)
            img2 = cv2.circle(frame, (x, y), n, (100, 100, 255), 2)
            if WINDOW:
                if ALL == 1:
                    for x, y in output[3][1:]:
                        x = int(x)
                        y = int(y)

                        mg2 = cv2.circle(frame, (x, y), n, 255, 2)
                cv2.imshow('img2', img2)
                cv2.waitKey(DELAY) & 0xff
        except:
            pass
    else:
        break

if SAVE == 1:
    d = {'mes': X, 'y': Y}
    df = pd.DataFrame(d)
    df.to_csv(os.path.join("../Output", "Data", f"{name}.csv"))
# print(len(Y))
cv2.destroyAllWindows()
cap.release()
