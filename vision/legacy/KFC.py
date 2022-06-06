
import os
import cv2

def bloop(fname, WINDOW=False):
    Video_FILE = os.path.join("../Input", fname)

    cap = cv2.VideoCapture(Video_FILE)

    X = []
    Y = []
    bbox = (0, 0, 0, 0)
    x0, y0 = -1, -1

    tracker = cv2.legacy.TrackerKCF_create()

    # tracker = cv2.legacy.TrackerMOSSE_create()
    T = []

    t = 0
    while (1):
        ret, frame = cap.read()
        frame = frame[600:1600, :]
        ok: int

        if bbox == (0, 0, 0, 0):
            bbox = cv2.selectROI(frame, False)
            ok = tracker.init(frame, bbox)
            cv2.destroyAllWindows()

        if ret == True:
            if not ok:
                break
            ok, bbox = tracker.update(frame)

            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

            x = ((bbox[0] + bbox[0] + bbox[2]) / 2)
            y = ((bbox[1] + bbox[1] + bbox[3]) / 2)
            if x0 == -1:
                x0, y0 = x, y
            X.append(x - x0)
            Y.append(y - y0)
            T.append(t)
            if WINDOW:
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                cv2.imshow("S", frame)

                cv2.waitKey(1) & 0xff
        else:
            break
        t +=1/30
    return X,Y,T

