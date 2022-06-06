import cv2
import numpy as np
def callback(x):
    pass
cap = cv2.VideoCapture(0)
cv2.namedWindow('image')
ret, frame = cap.read()


ilowH = 0
ihighH = 179

ilowS = 0
ihighS = 255
ilowV = 0
ihighV = 255

cv2.createTrackbar('lowH','image',ilowH,179,callback)
cv2.createTrackbar('highH','image',ihighH,179,callback)

cv2.createTrackbar('lowS','image',ilowS,255,callback)
cv2.createTrackbar('highS','image',ihighS,255,callback)

cv2.createTrackbar('lowV','image',ilowV,255,callback)
cv2.createTrackbar('highV','image',ihighV,255,callback)

n = int(50)
while True:

    ret, frame = cap.read()
    ilowH = cv2.getTrackbarPos('lowH', 'image')
    ihighH = cv2.getTrackbarPos('highH', 'image')
    ilowS = cv2.getTrackbarPos('lowS', 'image')
    ihighS = cv2.getTrackbarPos('highS', 'image')
    ilowV = cv2.getTrackbarPos('lowV', 'image')
    ihighV = cv2.getTrackbarPos('highV', 'image')
    frame = cv2.medianBlur(frame, 15)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([ilowH, ilowS, ilowV])
    higher_hsv = np.array([ihighH, ihighS, ihighV])
    mask = cv2.inRange(hsv, lower_hsv, higher_hsv)

    frame = cv2.bitwise_and(frame, frame, mask=mask)
    output = cv2.connectedComponentsWithStats(mask, 8, cv2.CV_32S)

    # show thresholded image


    for x,y in output[3][1:]:
        x = int(x)
        y = int(y)
        frame = cv2.rectangle(frame, (x - n, y - n), (x + n, y + n), 255, 2)
    cv2.imshow('image', frame)
    k = cv2.waitKey(1) & 0xFF  # large wait time to remove freezing
    if k == 113 or k == 27:
        break
