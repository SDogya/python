import cv2
import os
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

path = "H8.MOV"

SPIIIID = 0.5

name1 = os.path.join("../Output", "Traj", 'orig.mp4')
name2 = os.path.join('../Output', 'Traj', 'inverse.mp4')
name3 = os.path.join('../Output', 'Traj', 'combine.mp4')
# name4 = os.path.join('Output', 'Traj', '_.gif')
name4 = os.path.join('../Output', 'Traj', '_.mp4')
fps = 1


def Obr(fname, blur_size=30, ch="bloob", WINDOW=True):
    global fps
    X = []
    Y = []
    T = []
    t = 0
    DELAY = 1
    r = (0, 0, 0, 0)
    Video_FILE = os.path.join("../Input", fname)
    cap = cv2.VideoCapture(Video_FILE)
    x0, y0 = -1, -1
    n = int(blur_size)

    fps = cap.get(cv2.CAP_PROP_FPS)
    Duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps

    scale_percent = 100

    # оставь надеждуниже опустившийся
    if ch == "bloob":

        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 1000
        params.maxArea = 6000
        #
        # params.filterByConvexity = True
        # params.minConvexity = 0.5
        # params.maxConvexity = 1
        #
        # params.filterByCircularity = True
        # params.maxCircularity = 1
        # params.minCircularity = 0.6
        #
        # params.filterByInertia = True
        # params.minInertiaRatio = 0.3
        # params.maxInertiaRatio = 1

        ################### ################### ###################
        # q = 0
        # test = cv2.VideoCapture(Video_FILE)
        #
        # ret, frame = test.read()
        # cv2.imshow('image', frame)
        #
        # settings = {"RGB":[["R",0,255],
        #                    ["G",0,255],
        #                   ["B",0,255]]}
        # method = 1
        # cv2.namedWindow('image')
        # if "RGB" == "RGB":
        #     cv2.createTrackbar("minR", "image", settings["RGB"][0][1], settings["RGB"][0][2], callback)
        #     cv2.createTrackbar("minG", "image", settings["RGB"][1][1], settings["RGB"][1][2], callback)
        #     cv2.createTrackbar("minB", "image", settings["RGB"][2][1], settings["RGB"][2][2], callback)
        #     cv2.createTrackbar("maxR", "image", settings["RGB"][0][1], settings["RGB"][0][2], callback)
        #     cv2.createTrackbar("maxG", "image", settings["RGB"][1][1], settings["RGB"][1][2], callback)
        #     cv2.createTrackbar("maxB", "image", settings["RGB"][2][1], settings["RGB"][2][2], callback)
        # cv2.createTrackbar("b", "image", 0,200, callback)
        # cv2.createTrackbar("a", "image",0,255 , callback)
        # while q != 27:
        #     # a = cv2.getTrackbarPos("minR", "image",)
        #     # a1= cv2.getTrackbarPos("maxR", "image")
        #     # b = cv2.getTrackbarPos("minG", "image", )
        #     # b1 = cv2.getTrackbarPos("maxG", "image")
        #     # c = cv2.getTrackbarPos("minB", "image", )
        #     # c1 = cv2.getTrackbarPos("maxB", "image")
        #     a = cv2.getTrackbarPos("a", "image")
        #     b = cv2.getTrackbarPos("b", "image")
        #     out = cv2.addWeighted(frame, (a-100)/100, frame, 0, 255/2-b)
        #     # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     # lower_hsv = np.array([a, b, c])
        #     # higher_hsv = np.array([255-a1, 255-b1,255-c1])
        #     # mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
        #     # fframe = cv2.bitwise_and(frame, frame, mask=mask)
        #
        #
        #
        #     # cv2.imshow('image',fframe)
        #     cv2.imshow('image',out)
        #
        #     q= cv2.waitKey(1)
        #
        #     if q == 32 :
        #         ret, frame = test.read()
        #         fframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     ################### ################### ################### ###################
        detector = cv2.SimpleBlobDetector_create(params)
        k = 1
        r = cv2.selectROI(cv2.VideoCapture(Video_FILE).read()[1], False)

        cv2.destroyAllWindows()

        out1 = cv2.VideoWriter(name1, cv2.VideoWriter_fourcc(*'mp4v'), SPIIIID * fps, (int(r[2]), int(r[3])))
        # out12 = cv2.VideoWriter('orig.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps, (int(r[2]), int(r[3])))

        out2 = cv2.VideoWriter(name2, cv2.VideoWriter_fourcc(*'mp4v'), SPIIIID * fps, (int(r[2]), int(r[3])))

        out3 = cv2.VideoWriter(name3, cv2.VideoWriter_fourcc(*'mp4v'), SPIIIID * fps, (2 * int(r[2]), int(r[3])))
        # out22 = cv2.VideoWriter('inverse.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps, (int(r[2]), int(r[3])))

        while (1):

            ret, frame = cap.read()

            if ret == True:

                frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

                hsv = cv2.blur(frame, (n, n))
                # hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2RGB)
                hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)

                hsv = cv2.threshold(hsv, 0, 255,
                                    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

                hsv = cv2.bitwise_not(hsv)
                # resize image

                width = int(hsv.shape[1] * scale_percent / 100)
                height = int(hsv.shape[0] * scale_percent / 100)
                dim = (width, height)
                hsv = cv2.resize(hsv, dim, interpolation=cv2.INTER_AREA) # decment this if u need resize

                try:

                    keypoints = detector.detect(hsv)
                    # hsv = cv2.drawKeypoints(hsv, keypoints, np.array([]), (0, 0, 255),
                    #                         cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                    hsv = cv2.drawKeypoints(hsv, keypoints, np.array([]), (0, 0, 255),
                                            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                    x = np.array(cv2.KeyPoint_convert(keypoints)[:, 0]).mean()
                    y = np.array(cv2.KeyPoint_convert(keypoints)[:, 1]).mean()

                    if x0 == -1:
                        x0, y0 = x, y
                    T.append(t)
                    X.append((x - x0) * 100 / scale_percent * k)
                    Y.append((y - y0) * 100 / scale_percent * k)
                except:

                    pass
                if WINDOW:
                    out3.write(cv2.hconcat([frame, hsv]))
                    out2.write(hsv)
                    hsv = cv2.putText(hsv, f"{int(t / Duration * 100)}%",
                                      (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 255), 1
                                      )
                    cv2.imshow("Keypoints", hsv)
                    cv2.waitKey(DELAY) & 0xff

                    pass

            else:
                break
            out1.write(frame)
            # out12.write(frame)

            # out22.write(hsv)
            t += 1 / fps

        cv2.destroyAllWindows()
        cap.release()
        out1.release()
        # out12.release()
        out2.release()
        # out22.release()

    return X, Y, T


X, Y, T = Obr(path, 15)
# Y = np.random.randint(-100,100,100)
# T =np.random.randint(-100,100,100)

########################################################################################################

xplus = max(T) / 100 * 10
yplus = max(Y) / 100 * 10
fig = plt.figure()
axis = plt.axes(ylim=(min(Y) - yplus, max(Y) + yplus),
                xlim=(min(T) - xplus, max(T) + xplus))

xdata, ydata = [], []

l = len(Y)




def animate(i):
    print(i + 1, "/", l)
    xdata.append(T[i])
    ydata.append(Y[i])
    # line.set_data(xdata, ydata)
    fig.clear()
    ax = fig.add_subplot(111, ylim=(min(Y) - yplus, max(Y) + yplus), xlim=(min(T) - xplus, max(T) + xplus))

    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.xaxis.set_minor_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_minor_locator(ticker.NullLocator())
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    s = ax.scatter(xdata, ydata, s=4)


anim = animation.FuncAnimation(fig, animate, frames=len(Y), interval=0)
anim.save(name4, writer="ffmpeg", fps=50, dpi=200)

# cubic inter

# dpi 500 time 3:15
# dpi 100 time 0:50
# dpi 200 time 1:03
# without convert
# dpi 200 time 1:03

# nearest

# dpi 50 time 0:40
# #dpi 50 time 1:03

# import moviepy.editor as mp
#
# clip = mp.VideoFileClip(name4)
# clip.write_videofile(name4[:-3] + "mp4")
########################################################################################################
one = cv2.VideoCapture(name3)
two = cv2.VideoCapture(name4[:-3] + "mp4")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = one.get(cv2.CAP_PROP_FPS)
w1 = one.get(cv2.CAP_PROP_FRAME_WIDTH)
h1 = one.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(w1, h1)
w1 = w1 / 2
print(w1, h1)

out = cv2.VideoWriter('final.mp4', fourcc, 50, (int(w1 * 3.5), int(h1)))

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
