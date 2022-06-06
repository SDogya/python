import os
import numpy as np
import cv2
def callback(x):
    pass


def Obr(fname, blur_size=1, ch="bloob", WINDOW=False):
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

        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 500
        params.maxArea = 6000

        params.filterByConvexity = True
        params.minConvexity = 0.5
        params.maxConvexity = 1

        params.filterByCircularity = True
        params.maxCircularity = 1
        params.minCircularity = 0.6

        params.filterByInertia = True
        params.minInertiaRatio = 0.3
        params.maxInertiaRatio = 1

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
        R=1
        while (1):

            ret, frame = cap.read()

            if ret == True:

                while r == (0, 0, 0, 0):
                    r = cv2.selectROI(frame, False)
                    cv2.destroyAllWindows()
                frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
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
                hsv = cv2.blur(frame, (n, n))
                hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2RGB)
                hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
                hsv = cv2.threshold(hsv, 0, 255,
                                    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                hsv = cv2.bitwise_not(hsv)
                # resize image
                width = int(frame.shape[1] * scale_percent / 100)
                height = int(frame.shape[0] * scale_percent / 100)
                dim = (width, height)
                hsv = cv2.resize(hsv, dim, interpolation=cv2.INTER_AREA)
                try:

                    keypoints = detector.detect(hsv)
                    hsv = cv2.drawKeypoints(hsv, keypoints, np.array([]), (0, 0, 255),
                                            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                    x = np.array(cv2.KeyPoint_convert(keypoints)[:, 0]).mean()
                    y = np.array(cv2.KeyPoint_convert(keypoints)[:, 1]).mean()

                    if x0 == -1:
                        x0, y0 = x, y
                    T.append(t)
                    X.append((x - x0)*100/scale_percent*k)
                    Y.append((y - y0)*100/scale_percent*k)
                except:
                    pass
                if WINDOW:
                    hsv = cv2.putText(hsv, f"{int(t / Duration * 100)}%",
                                      (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 255), 1
                                      )
                    cv2.imshow("Keypoints", hsv)
                    cv2.waitKey(DELAY) & 0xff
                    pass
            else:
                break
            t += 1 / fps

        cv2.destroyAllWindows()
        cap.release()
    elif ch == "csrt":

        default_params = {
            'padding': 3.,
            'template_size': 200.,
            'gsl_sigma': 1.,
            'hog_orientations': 9.,
            'num_hog_channels_used': 18,
            'hog_clip': 2.0000000298023224e-01,
            'use_hog': 1,
            'use_color_names': 1,
            'use_gray': 1,
            'use_rgb': 0,
            'window_function': 'hann',
            'kaiser_alpha': 3.7500000000000000e+00,
            'cheb_attenuation': 45.,
            'filter_lr': 1.9999999552965164e-02,
            'admm_iterations': 4,
            'number_of_scales': 100,
            'scale_sigma_factor': 0.25,
            'scale_model_max_area': 512.,
            'scale_lr': 2.5000000372529030e-02,
            'scale_step': 1.02,
            'use_channel_weights': 1,
            'weights_lr': 1.9999999552965164e-02,
            'use_segmentation': 1,
            'histogram_bins': 16,
            'background_ratio': 2,
            'histogram_lr': 3.9999999105930328e-02,
            'psr_threshold': 3.5000000149011612e-02,
        }
        # modify
        params = {
            #     'scale_lr': 0.5,
            #     'number_of_scales': 1000,
            # 'use_rgb': 1,
        }
        params = {**default_params, **params}
        cv2.legacy.TrackerCSRT_Params = params
        tracker = cv2.legacy.TrackerCSRT_create()

        while (1):

            ret, frame = cap.read()
            while r == (0, 0, 0, 0):
                r = cv2.selectROI(frame, False)
                cv2.destroyAllWindows()
            try:
                frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
            except:
                pass

            if cv2.waitKey(1) & 0xff == 114:
                bbox = (0, 0, 0, 0)
            if bbox == (0, 0, 0, 0):
                hsv = cv2.blur(frame, (n, n))
                hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2RGB)
                hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
                hsv = cv2.threshold(hsv, 0, 255,
                                    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                hsv = cv2.bitwise_not(hsv)

                bbox = cv2.selectROI(hsv, True)
                tracker = cv2.legacy.TrackerCSRT_create()
                ok = tracker.init(hsv, bbox)
                cv2.destroyAllWindows()

            if ret == True:
                if not ok:
                    break
                hsv = cv2.blur(frame, (n, n))
                hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2RGB)
                hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
                hsv = cv2.threshold(hsv, 0, 255,
                                    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                hsv = cv2.bitwise_not(hsv)
                ok, bbox = tracker.update(hsv)

                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

                x = ((bbox[0] + bbox[0] + bbox[2]) / 2)
                y = ((bbox[1] + bbox[1] + bbox[3]) / 2)
                if x0 == -1:
                    x0, y0 = x, y

                T.append(t)
                X.append(x - x0)
                Y.append(y - y0)

                if WINDOW:
                    hsv = cv2.putText(hsv, f"{int(t / Duration * 100)}%",
                                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 255), 1
                                        )
                    cv2.rectangle(hsv, p1, p2, (255, 0, 0), 2, 1)
                    cv2.imshow("S", hsv)


            else:
                break
            t += 1 / fps
    elif ch == "kfc":
        tracker = cv2.legacy.TrackerKCF_create()
        while (1):
            ret, frame = cap.read()
            while r == (0, 0, 0, 0):
                r = cv2.selectROI(frame, False)
                cv2.destroyAllWindows()
            try:
                frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
            except:
                pass
            ok: int
            if cv2.waitKey(1) & 0xff == 114:
                bbox = (0, 0, 0, 0)
            if bbox == (0, 0, 0, 0):
                bbox = cv2.selectROI(frame, True)
                tracker = cv2.legacy.TrackerKCF_create()
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
                    frame = cv2.putText(frame, f"{int(t / Duration * 100)}%",
                                      (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 255), 1
                                      )
                    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                    cv2.imshow("S", frame)

                    cv2.waitKey(1) & 0xff
            else:
                break
            t += 1 / fps
    print(len(T))
    return X, Y, T
#super duper backup
# """import os
# import numpy as np
# import cv2
# def callback(mes):
#     pass
#
#
# def Obr(fname, blur_size=1, ch="bloob", WINDOW=False):
#     X = []
#     Y = []
#     T = []
#     t = 0
#     DELAY = 1
#     r = (0, 0, 0, 0)
#     bbox = (0, 0, 0, 0)
#     Video_FILE = os.path.join("Input", fname)
#     cap = cv2.VideoCapture(Video_FILE)
#     x0, y0 = -1, -1
#     n = int(blur_size)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     Duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
#
#     scale_percent = 100
#     # оставь надеждуниже опустившийся
#     if ch == "bloob":
#
#         params = cv2.SimpleBlobDetector_Params()
#         params.filterByArea = True
#         params.minArea = 500
#         params.maxArea = 6000
#
#         params.filterByConvexity = True
#         params.minConvexity = 0.5
#         params.maxConvexity = 1
#
#         params.filterByCircularity = True
#         params.maxCircularity = 1
#         params.minCircularity = 0.6
#
#         params.filterByInertia = True
#         params.minInertiaRatio = 0.3
#         params.maxInertiaRatio = 1
#
#         ################### ################### ###################
#         # q = 0
#         # test = cv2.VideoCapture(Video_FILE)
#         #
#         # ret, frame = test.read()
#         # cv2.imshow('image', frame)
#         #
#         # settings = {"RGB":[["R",0,255],
#         #                    ["G",0,255],
#         #                   ["B",0,255]]}
#         # method = 1
#         # cv2.namedWindow('image')
#         # if "RGB" == "RGB":
#         #     cv2.createTrackbar("minR", "image", settings["RGB"][0][1], settings["RGB"][0][2], callback)
#         #     cv2.createTrackbar("minG", "image", settings["RGB"][1][1], settings["RGB"][1][2], callback)
#         #     cv2.createTrackbar("minB", "image", settings["RGB"][2][1], settings["RGB"][2][2], callback)
#         #     cv2.createTrackbar("maxR", "image", settings["RGB"][0][1], settings["RGB"][0][2], callback)
#         #     cv2.createTrackbar("maxG", "image", settings["RGB"][1][1], settings["RGB"][1][2], callback)
#         #     cv2.createTrackbar("maxB", "image", settings["RGB"][2][1], settings["RGB"][2][2], callback)
#         # cv2.createTrackbar("b", "image", 0,200, callback)
#         # cv2.createTrackbar("a", "image",0,255 , callback)
#         # while q != 27:
#         #     # a = cv2.getTrackbarPos("minR", "image",)
#         #     # a1= cv2.getTrackbarPos("maxR", "image")
#         #     # b = cv2.getTrackbarPos("minG", "image", )
#         #     # b1 = cv2.getTrackbarPos("maxG", "image")
#         #     # c = cv2.getTrackbarPos("minB", "image", )
#         #     # c1 = cv2.getTrackbarPos("maxB", "image")
#         #     a = cv2.getTrackbarPos("a", "image")
#         #     b = cv2.getTrackbarPos("b", "image")
#         #     out = cv2.addWeighted(frame, (a-100)/100, frame, 0, 255/2-b)
#         #     # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         #     # lower_hsv = np.array([a, b, c])
#         #     # higher_hsv = np.array([255-a1, 255-b1,255-c1])
#         #     # mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
#         #     # fframe = cv2.bitwise_and(frame, frame, mask=mask)
#         #
#         #
#         #
#         #     # cv2.imshow('image',fframe)
#         #     cv2.imshow('image',out)
#         #
#         #     q= cv2.waitKey(1)
#         #
#         #     if q == 32 :
#         #         ret, frame = test.read()
#         #         fframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         #     ################### ################### ################### ###################
#         detector = cv2.SimpleBlobDetector_create(params)
#         k = 1
#         R=1
#         while (1):
#
#             ret, frame = cap.read()
#
#             if ret == True:
#
#                 while r == (0, 0, 0, 0):
#                     r = cv2.selectROI(frame, False)
#                     cv2.destroyAllWindows()
#                 frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
#                 # while k==0:
#                 #     k = cv2.selectROI(frame, False)
#                 #     k= 7.5 /(k[2])
#                 #     cv2.destroyAllWindows()
#                 #     print(k)
#                 # while R == 0:
#                 #         R = cv2.selectROI(frame, False)
#                 #         R = (R[2])*k
#                 #         cv2.destroyAllWindows()
#                 #         print(R)
#                 hsv = cv2.blur(frame, (n, n))
#                 hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2RGB)
#                 # hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
#                 # hsv = cv2.threshold(hsv, 0, 255,
#                 #                     cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
#                 # hsv = cv2.bitwise_not(hsv)
#                 # resize image
#                 width = int(frame.shape[1] * scale_percent / 100)
#                 height = int(frame.shape[0] * scale_percent / 100)
#                 dim = (width, height)
#                 hsv = cv2.resize(hsv, dim, interpolation=cv2.INTER_AREA)
#                 try:
#
#                     keypoints = detector.detect(hsv)
#                     hsv = cv2.drawKeypoints(hsv, keypoints, np.array([]), (0, 0, 255),
#                                             cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#                     mes = np.array(cv2.KeyPoint_convert(keypoints)[:, 0]).mean()
#                     y = np.array(cv2.KeyPoint_convert(keypoints)[:, 1]).mean()
#
#                     if x0 == -1:
#                         x0, y0 = mes, y
#                     T.append(t)
#                     X.append((mes - x0)*100/scale_percent*k)
#                     Y.append((y - y0)*100/scale_percent*k)
#                 except:
#                     pass
#                 if WINDOW:
#                     hsv = cv2.putText(hsv, f"{int(t / Duration * 100)}%",
#                                       (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 255), 1
#                                       )
#                     cv2.imshow("Keypoints", hsv)
#                     cv2.waitKey(DELAY) & 0xff
#                     pass
#             else:
#                 break
#             t += 1 / fps
#
#         cv2.destroyAllWindows()
#         cap.release()
#     elif ch == "csrt":
#
#         default_params = {
#             'padding': 3.,
#             'template_size': 200.,
#             'gsl_sigma': 1.,
#             'hog_orientations': 9.,
#             'num_hog_channels_used': 18,
#             'hog_clip': 2.0000000298023224e-01,
#             'use_hog': 1,
#             'use_color_names': 1,
#             'use_gray': 1,
#             'use_rgb': 0,
#             'window_function': 'hann',
#             'kaiser_alpha': 3.7500000000000000e+00,
#             'cheb_attenuation': 45.,
#             'filter_lr': 1.9999999552965164e-02,
#             'admm_iterations': 4,
#             'number_of_scales': 100,
#             'scale_sigma_factor': 0.25,
#             'scale_model_max_area': 512.,
#             'scale_lr': 2.5000000372529030e-02,
#             'scale_step': 1.02,
#             'use_channel_weights': 1,
#             'weights_lr': 1.9999999552965164e-02,
#             'use_segmentation': 1,
#             'histogram_bins': 16,
#             'background_ratio': 2,
#             'histogram_lr': 3.9999999105930328e-02,
#             'psr_threshold': 3.5000000149011612e-02,
#         }
#         # modify
#         params = {
#             #     'scale_lr': 0.5,
#             #     'number_of_scales': 1000,
#             # 'use_rgb': 1,
#         }
#         params = {**default_params, **params}
#         cv2.legacy.TrackerCSRT_Params = params
#         tracker = cv2.legacy.TrackerCSRT_create()
#
#         while (1):
#
#             ret, frame = cap.read()
#             while r == (0, 0, 0, 0):
#                 r = cv2.selectROI(frame, False)
#                 cv2.destroyAllWindows()
#             try:
#                 frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
#             except:
#                 pass
#             if cv2.waitKey(1) & 0xff == 114:
#                 bbox = (0, 0, 0, 0)
#             if bbox == (0, 0, 0, 0):
#                 bbox = cv2.selectROI(frame, True)
#                 tracker = cv2.legacy.TrackerCSRT_create()
#                 ok = tracker.init(frame, bbox)
#                 cv2.destroyAllWindows()
#
#             if ret == True:
#                 if not ok:
#                     break
#                 ok, bbox = tracker.update(frame)
#
#                 p1 = (int(bbox[0]), int(bbox[1]))
#                 p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
#
#                 mes = ((bbox[0] + bbox[0] + bbox[2]) / 2)
#                 y = ((bbox[1] + bbox[1] + bbox[3]) / 2)
#                 if x0 == -1:
#                     x0, y0 = mes, y
#
#                 T.append(t)
#                 X.append(mes - x0)
#                 Y.append(y - y0)
#
#                 if WINDOW:
#                     frame = cv2.putText(frame, f"{int(t / Duration * 100)}%",
#                                         (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 255), 1
#                                         )
#                     cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
#                     cv2.imshow("S", frame)
#
#
#             else:
#                 break
#             t += 1 / fps
#     elif ch == "kfc":
#         tracker = cv2.legacy.TrackerKCF_create()
#         while (1):
#             ret, frame = cap.read()
#             while r == (0, 0, 0, 0):
#                 r = cv2.selectROI(frame, False)
#                 cv2.destroyAllWindows()
#             try:
#                 frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
#             except:
#                 pass
#             ok: int
#             if cv2.waitKey(1) & 0xff == 114:
#                 bbox = (0, 0, 0, 0)
#             if bbox == (0, 0, 0, 0):
#                 bbox = cv2.selectROI(frame, True)
#                 tracker = cv2.legacy.TrackerKCF_create()
#                 ok = tracker.init(frame, bbox)
#                 cv2.destroyAllWindows()
#
#             if ret == True:
#                 if not ok:
#                     break
#                 ok, bbox = tracker.update(frame)
#
#                 p1 = (int(bbox[0]), int(bbox[1]))
#                 p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
#
#                 mes = ((bbox[0] + bbox[0] + bbox[2]) / 2)
#                 y = ((bbox[1] + bbox[1] + bbox[3]) / 2)
#                 if x0 == -1:
#                     x0, y0 = mes, y
#                 X.append(mes - x0)
#                 Y.append(y - y0)
#                 T.append(t)
#                 if WINDOW:
#                     frame = cv2.putText(frame, f"{int(t / Duration * 100)}%",
#                                       (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 255), 1
#                                       )
#                     cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
#                     cv2.imshow("S", frame)
#
#                     cv2.waitKey(1) & 0xff
#             else:
#                 break
#             t += 1 / fps
#     print(len(T))
#     return X, Y, T
# """