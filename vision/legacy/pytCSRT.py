import pandas as pd
import os
import cv2

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


def beep(fname, WINDOW=False):
    Video_FILE = os.path.join("../Input", fname)

    cap = cv2.VideoCapture(Video_FILE)
    fps = cap.get(cv2.CAP_PROP_FPS)
    Duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps



    X = []
    Y = []
    bbox = (0, 0, 0, 0)
    x0, y0 = -1, -1
    cv2.legacy.TrackerCSRT_Params = params
    tracker = cv2.legacy.TrackerCSRT_create()

    T = []
    t = 0
    while (1):
        ret, frame = cap.read()

        ok: int

        if cv2.waitKey(1) & 0xff==114:
                    bbox = (0, 0, 0, 0)
        if bbox == (0, 0, 0, 0):
            bbox = cv2.selectROI(frame, False)
            tracker = cv2.legacy.TrackerCSRT_create()
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

            T.append(t)
            X.append(x - x0)
            Y.append(y - y0)

            if WINDOW:
                frame = cv2.putText(frame, f"{int(t / Duration * 100)}%",
                                  (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 255), 1
                                  )
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                cv2.imshow("S", frame)


        else:
            break
        t += 1 / fps
    return X,Y,T

